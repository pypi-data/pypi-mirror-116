from cartesio.helpers.observer import Observer
from cartesio.utils.stacking import GenerationStacker
from cartesio.utils.json_utils import write

from abc import ABC, abstractmethod
from cartesio.utils.saving import JsonSaver
from cania_utils.disk import Disk
from cania_utils.stamp import eventid

import os


class CallbackABC(Observer, ABC):
    def update(self, event):
        self._callback(event['name'], event['content'])

    @abstractmethod
    def _callback(self, e_name, e_content):
        pass


class CallbackVerbose(CallbackABC):
    def __init__(self, frequency=1):
        self.frequency = frequency

    def _callback(self, e_name, e_content):
        if e_name != 'on_evaluation_end':
            return

        if e_content.n % self.frequency != 0:
            return

        elite = e_content.get_best()
        n = e_content.n
        fitness = elite.fitness["fitness"]
        time = elite.fitness["time"]
        fps = 1./time
        print(f'[G {n:04}] {fitness:.4f} {time:.6f}s {int(round(fps))}fps')


class CallbackSave(CallbackABC):
    def __init__(self, decoder, workdir, dataset, frequency=1):
        self.decoder = decoder
        self.workdir = Disk(workdir).next(eventid()).location
        self.json_saver = JsonSaver(dataset, decoder)
        self.stacker = GenerationStacker()
        self.frequency = frequency

    def save_population(self, population, gen_n):
        filename = f'G{gen_n}.json'
        filepath = self.workdir / filename
        self.json_saver.save_population(filepath, population)

    def save_elite(self, elite):
        filepath = self.workdir / 'elite.json'
        self.json_saver.save_individual(filepath, elite)

    def stack_files(self):
        generations = [f.path for f in os.scandir(self.workdir) if f.is_file() and f.name != 'elite.json' and f.name != 'history.json']
        history = self.stacker.stack(generations)
        filename = 'history.json'
        filepath = self.workdir / filename
        write(filepath, history, indent=None)
        for generation in generations:
            os.remove(generation)

    def _callback(self, e_name, e_content):
        if e_name != 'on_evaluation_end':
            return

        if e_content.n % self.frequency != 0:
            return

        for p_idx, p in e_content.get_populations():
            self.save_population(p.get_individuals(), e_content.n)
