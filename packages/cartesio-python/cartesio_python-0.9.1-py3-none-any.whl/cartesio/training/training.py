from cartesio.model.ea.genome import GenomeMetadata
from cartesio.applications.CGPIP import CGPIP
from cartesio.applications.CGPC import CGPC
from cartesio.model.callback import CallbackVerbose, CallbackSave
from cartesio.training.dataset import DatasetFactory
from cartesio.utils.viewer import GenomeViewer
from cania_utils.plot import plot_predictions


class DefaultTraining(object):
    def __init__(self, dataset, mutation_rate=0.15, mutation_rate_output=0.2, workdir=None, endpoint=None):
        self.dataset = DatasetFactory.create(dataset, True, True)
        metadata = GenomeMetadata(self.dataset.n_inputs, 10, 1, 2, 2)
        if endpoint == 'C' or endpoint == 'count':
            self.model = CGPC(metadata, mutation_rate, mutation_rate_output)
        else:
            self.model = CGPIP(metadata, mutation_rate, mutation_rate_output)
        self.callbacks = []
        self.callbacks.append(CallbackVerbose(frequence=10))
        self.viewer = GenomeViewer(metadata, self.model.decoder.function_set)
        if workdir:
            self.callbacks.append(CallbackSave(self.model.decoder, workdir, dataset, frequence=10))

    def run(self, generations, populations, individuals):
        train_x = self.dataset.get_train_x()
        train_y = self.dataset.get_train_y()
        return self.model.fit(train_x, train_y, generations, populations, individuals, callbacks=self.callbacks)

    def display_genome(self, individual, only_active=False, jupyter=False):
        return self.viewer.get_graph(individual, only_active, jupyter)

    def _predict(self, dataset, individual):
        return self.model.predict(dataset, individual)

    def predict_on_train_x(self, individual):
        return self._predict(self.dataset.get_train_x(), individual)

    def predict_on_test_x(self, individual):
        return self._predict(self.dataset.get_test_x(), individual)

    def contours_on_test_x(self, individual):
        originals = self.dataset.get_testing_set().preview_images
        p = self.predict_on_test_x(individual)
        for i in range(len(originals)):
            plot_predictions(originals[i], p[i][0])

    def evaluate_on_test_x(self, individual, plot_predictions=False):
        test_y = self.dataset.get_test_y()

        p = self.predict_on_test_x(individual)
        f = self.model.evaluate(test_y, [p])

        if plot_predictions:
            originals = self.dataset.get_testing_set().preview_images
            for i in range(len(originals)):
                plot_predictions(originals[i], p[i][0])
        return f

    '''def evaluate_on_train_x(self, individual):
        return self.model.evaluate(self.dataset.get_train_x(), self.dataset.get_train_y(), individual)

    def evaluate_on_test_x(self, individual):
        return self.model.evaluate(self.dataset.get_test_x(), self.dataset.get_test_y(), individual)

    def get_dataset_name(self):
        return self.dataset.get_name()

    def save(self, genome, dataset_location):
        filename = str(self.workdir.location / 'elite.json')
        self.genome_saver.save(genome, self.model.decoder, filename, dataset_location)
    '''