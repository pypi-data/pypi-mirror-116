import numpy as np
import simplejson
import ast
from typing import List

from cartesio.model.ea.genome import GenomeMetadata, Genome
from cartesio.model.ea.decoder import Decoder, EndpointedDecoder
from cartesio.model.endpoint import EndpointCounting, EndpointWatershed
from cartesio.cv.function_set import EmptyFunctionSet


def read(filename):
    with open(filename, 'rb') as json_file:
        json_data = simplejson.load(json_file)
        return json_data


def write(filename, json_data, indent=4):
    with open(filename, 'w') as json_file:
        simplejson.dump(json_data, json_file, indent=indent)


''' Genome Metadata '''


def to_metadata(json_data):
    return GenomeMetadata(
        json_data['n_in'],
        json_data['columns'],
        json_data['n_out'],
        json_data['n_conn'],
        json_data['n_para']
    )


''' Function Set '''


def to_function_set(json_data):
    function_set = EmptyFunctionSet()
    for f_name in json_data:
        function_set.add_function(f_name)
    return function_set


def to_endpoint(json_data):
    if json_data == 'W':
        return EndpointWatershed()
    if json_data == 'C':
        return EndpointCounting()


def to_decoder(json_data):
    metadata = to_metadata(json_data['metadata'])
    function_set = to_function_set(json_data['functions'])
    if json_data['_endpoint']:
        endpoint = to_endpoint(json_data['_endpoint'])
        return EndpointedDecoder(metadata, function_set, endpoint)
    return Decoder(metadata, function_set)


def to_genome(json_data):
    sequence = np.asarray(ast.literal_eval(json_data['sequence']))
    return Genome(sequence=sequence)


def from_individual(individual):
    return {
        "sequence": simplejson.dumps(individual.sequence.tolist()),
        "fitness": individual.fitness
    }


def from_population(population: List):
    json_data = []
    for individual_idx, individual in population:
        json_data.append(from_individual(individual))
    return json_data


def from_dataset(dataset):
    return {
        "name": dataset.get_name(),
        "label_name": dataset.get_labels(),
        "indices": dataset.get_indices()
    }
