import pandas as pd
import numpy as np
import cv2
from dataclasses import dataclass

from micromind.io.drive.directory import WorkingDirectory
from micromind.imagej import read_ellipses_from_csv
from micromind.io.image import imread_grayscale, imread_color, imread_tiff
from micromind.cv.image import imnew, fill_ellipses_as_labels, overlay, split_channels

from cartesio.dataset.meta import DatasetMeta
from cartesio.dataset.dataset import Dataset

DEFAULT_DATASET_FILENAME = 'dataset.csv'


@dataclass
class DataReader:
    wordir: WorkingDirectory
    datatype: str
    dataformat: str

    def _read_grayscale(self, filepath):
        return imread_grayscale(filepath)

    def _read_rgb(self, filepath):
        return imread_color(filepath)

    def _read_labels(self, filepath):
        image = cv2.imread(filepath, cv2.IMREAD_ANYDEPTH)
        return image, image.max()

    def _read_channels(self, filepath):
        image = imread_tiff(filepath)
        return image

    def _read_ellipses(self, filepath, w, h):
        dataframe = pd.read_csv(filepath)
        ellipses = read_ellipses_from_csv(dataframe, scale=1.0, ellipse_scale=1.0)
        label_mask = imnew((h, w))
        fill_ellipses_as_labels(label_mask, ellipses)
        return label_mask, len(ellipses)

    def read(self, dataname, w=None, h=None):
        filepath = str(self.pwd / dataname)
        if self.datatype == 'image':
            if self.dataformat == 'grayscale':
                image = self._read_grayscale(filepath)
                return [image], image.shape[1], image.shape[0], image, None
            if self.dataformat == 'rgb':
                image = self._read_rgb(filepath)
                return split_channels(image), image.shape[1], image.shape[0], image, None
            if self.dataformat == 'labels':
                image, n = self._read_labels(filepath)
                return [image], image.shape[1], image.shape[0], image, n
            if self.dataformat == 'channels':
                image = self._read_channels(filepath)
                channels = [channel for channel in image]
                preview = cv2.merge((channels[0], channels[1], channels[2]))
                return channels, image.shape[2], image.shape[1], preview, None

        if self.datatype == 'csv':
            if self.dataformat == 'ellipse':
                image, n = self._read_ellipses(filepath, w, h)
                return [image], w, h, None, n

        raise AttributeError(f'combining {self.datatype} and {self.dataformat} is not handled yet')


@dataclass
class DatasetReader(WorkingDirectory):
    counting: bool = False
    preview: bool = False

    def __post_init__(self, path):
        super().__post_init__(path)

    def __init__(self, dataset_path, counting=False, preview=False):
        super().__init__(dataset_path)
        self._read_meta()
        self.counting = counting
        self.preview = preview
        if self.preview:
            self.preview_dir = self.next('_preview')

    def _read_meta(self):
        meta = DatasetMeta.read(self._path)
        self.name = meta['name']
        self.mode = meta['mode']
        self.label_name = meta['label_name']
        self.input_reader = DataReader(self, meta['input']['type'], meta['input']['format'])
        self.label_reader = DataReader(self, meta['label']['type'], meta['label']['format'])

    def read_dataset(self, dataset_filename=DEFAULT_DATASET_FILENAME, indices=None):
        dataset = Dataset(self.name, self.label_name, indices)
        if self.mode == 'dataframe':
            return self._read_from_dataframe(dataset_filename, dataset, indices)
        if self.mode == 'auto':
            return self._read_auto(dataset)
        raise AttributeError(f'{self.mode} is not handled yet')

    def _read_from_dataframe(self, dataset_filename, dataset, indices):
        dataframe = self.read(dataset_filename)
        self._read_training_set(dataframe, dataset, indices)
        self._read_testing_set(dataframe, dataset)
        return dataset

    def _read_auto(self, dataset):
        pass

    def _read_training_set(self, dataframe, dataset, indices):
        dataframe = dataframe[dataframe['set'] == 'training']
        dataframe.reset_index(inplace=True)
        for row in dataframe.itertuples():
            if indices is None or row.Index in indices:
                x, w, h, preview, _ = self.input_reader.read(row.input)
                dataset.n_inputs = len(x)
                y, _, _, _, n = self.label_reader.read(row.label, w, h)
                if self.counting:
                    y = [y[0], n]
                dataset.append_training_element(x, y)
                dataset.append_training_image(preview)
                if self.preview:
                    preview = overlay(preview, y[0].astype(np.uint8))
                    self.preview_dir.write(f"{self.label_name}_train_{row.Index}.png", preview)

    def _read_testing_set(self, dataframe, dataset):
        dataframe = dataframe[dataframe['set'] == 'testing']
        dataframe.reset_index(inplace=True)
        for row in dataframe.itertuples():
            x, w, h, preview, _ = self.input_reader.read(row.input)
            y, _, _, _, n = self.label_reader.read(row.label, w, h)
            if self.counting:
                y = [y[0], n]
            dataset.append_testing_element(x, y)
            dataset.append_testing_image(preview)
            if self.preview:
                preview = overlay(preview, y[0].astype(np.uint8))
                self.preview_dir.write(f"{self.label_name}_test_{row.Index}.png", preview)


if __name__ == "__main__":
    directory = r'/home/local/INSERM/kevin.cortacero/1_WORKSPACE/Dataset/Cellpose/CellImageLibrary'
    dataset_reader = DatasetReader(directory)