
from cartesio.model.cgp import EndpointedCGP
from cartesio.model.endpoint import EndpointCounting
from cartesio.model.ea.mutation import MutationAllRandom, MutationClassic
from cartesio.model.ea.strategy import OnePlusLambda
from cartesio.model.ea.fitness import FitnessCountPrecision, FitnessCountIOU
from cartesio.model.ea.genome import GenomeFactory, GenomeMetadata
from cartesio.cv.opencv_set import OPENCV_SET


# Cartesian Genetic Programming for Counting
class CGPC(EndpointedCGP):
    def __init__(self, metadata=GenomeMetadata(), mutation_rate=0.15, output_mutation_rate=0.2, mask_metric='precision'):
        self.mutation_rate = mutation_rate
        self.output_mutation_rate = output_mutation_rate
        self.mask_metric = mask_metric
        super().__init__(metadata, OPENCV_SET, EndpointCounting())

    def _compose_genetic_algorithm(self):
        self.genetic_algorithm.set_initialization(MutationAllRandom(self.decoder._m, self.decoder.function_set.n_functions), GenomeFactory(self.decoder._m.prototype))
        self.genetic_algorithm.set_mutation(MutationClassic(self.decoder._m, self.decoder.function_set.n_functions, self.mutation_rate, self.output_mutation_rate))
        self.genetic_algorithm.set_evolution_strategy(OnePlusLambda())
        if self.mask_metric == 'precision':
            self.genetic_algorithm.set_fitness(FitnessCountPrecision())
        elif self.mask_metric == 'iou':
            self.genetic_algorithm.set_fitness(FitnessCountIOU())
