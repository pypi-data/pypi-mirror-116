
from cartesio.utils.json_utils import read, write

META_FILENAME = 'META.json'


class DatasetMeta(object):
    @staticmethod
    def write(filepath, name, input_type, input_format, label_type, label_format, label_name, scale=1.0, mode='dataframe'):
        json_data = {
            'name': name,
            'scale': scale,
            'label_name': label_name,
            'mode': mode,
            'input': {
                'type': input_type,
                'format': input_format
            },
            'label': {
                'type': label_type,
                'format': label_format
            }
        }
        write(filepath + '/' + META_FILENAME, json_data)

    @staticmethod
    def read(filepath):
        return read(filepath / META_FILENAME)
