"""
Example:
evaluation_experiment = Evaluate(backend=tracking_backend,
                                 model=training_experiment.model,
                                 loaders=[x,y],
                                 data_parameters = data_loader)

target_cube, pred_cube = evaluation_experiment.run()
"""

import os
import time
from typing import List, Dict
import logging

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import torch

from sapsan.core.models import Experiment, ExperimentBackend, Estimator
from sapsan.lib.backends.fake import FakeBackend
from sapsan.utils.plot import pdf_plot, cdf_plot, slice_plot
from sapsan.utils.shapes import combine_cubes, slice_of_cube


class Evaluate(Experiment):
    def __init__(self,                 
                 model: Estimator,
                 loaders: np.ndarray,
                 data_parameters,
                 backend = FakeBackend(),
                 cmap: str = 'plasma',
                 flat: bool = False):
        self.model = model
        self.backend = backend
        self.experiment_metrics = dict()
        self.data_parameters = data_parameters
        self.input_size = self.data_parameters.input_size
        self.batch_size = self.data_parameters.batch_size
        self.batch_num = self.data_parameters.batch_num
        self.cmap = cmap
        self.axis = len(self.input_size)
        
        self.loaders = loaders
        try:
            self.inputs = self.loaders[0]
            self.targets = self.loaders[1]
        except:
            raise TypeError("Evaluate only accepts 'lists' and 'np.ndarrays' for loaders")
        
        self.flat = flat
        if self.flat: self.n_output_channels = self.targets.shape[0] #flat arrays don't have batches
        elif len(self.targets.shape)<(self.axis+2): self.n_output_channels = 1
        else: self.n_output_channels = self.targets.shape[1]

        self.artifacts = []
        
    def get_metrics(self) -> Dict[str, float]:
        if 'train' in self.model.metrics():
            self.experiment_metrics['train - final epoch'] = self.model.metrics()['final epoch']
            for metric, value in self.model.metrics()['train'].items():
                if "/" in metric: metric = metric.replace("/", " over ")
                self.experiment_metrics['train - %s'%metric] = value
        else: self.experiment_metrics = {**self.experiment_metrics, **self.model.metrics()}
            
        return self.experiment_metrics

    def get_parameters(self) -> Dict[str, str]:
        return {
            **self.data_parameters.get_parameters(), 
            **self.model.config.parameters, 
            **{"n_output_channels": str(self.n_output_channels)}            
        }        

    def get_artifacts(self) -> List[str]:
        return self.artifacts

    def _cleanup(self):
        for artifact in self.artifacts:
            os.remove(artifact)
        return len(self.artifacts)

    def run(self) -> dict:
        start = time.time()
        
        self.backend.start('evaluate')

        pred = self.model.predict(self.inputs)
        
        end = time.time()
        runtime = end - start
        self.backend.log_metric("runtime", runtime)
                
        pdf = pdf_plot([pred, self.targets], names=['prediction', 'target'])
        pdf.savefig("pdf_plot.png")
        self.artifacts.append("pdf_plot.png")

        try:
            cdf = cdf_plot([pred, self.targets], names=['prediction', 'target'])
            cdf.savefig("cdf_plot.png")
            self.artifacts.append("cdf_plot.png")
        except Exception as e:
            logging.warning(e)

        if self.flat: pred_slice, target_slice, pred_cube, target_cube = self.flatten(pred)
        else: pred_slice, target_slice, pred_cube, target_cube = self.split_batch(pred)
                
        slices = slice_plot([pred_slice, target_slice], names=['prediction', 'target'], cmap=self.cmap)
        slices.savefig("slices_plot.png")
        self.artifacts.append("slices_plot.png")        
        
        self.experiment_metrics["eval - MSE Loss"] = np.square(np.subtract(target_cube, pred_cube)).mean()         

        for metric, value in self.get_metrics().items():
            self.backend.log_metric(metric, value)

        for param, value in self.get_parameters().items():
            self.backend.log_parameter(param, value)

        for artifact in self.artifacts:
            self.backend.log_artifact(artifact)
            
        self.backend.end()
        self._cleanup()
        
        print("eval - runtime: ", runtime)
        
        return target_cube, pred_cube
    
    
    def flatten(self, pred):
        if self.axis == 3:
            cube_shape = (self.n_output_channels, self.input_size[0],
                          self.input_size[1], self.input_size[2])
        if self.axis == 2: 
            cube_shape = (self.n_output_channels, self.input_size[0], self.input_size[1])
            
        pred_cube = pred.reshape(cube_shape)
        target_cube = self.targets.reshape(cube_shape)

        pred_slice = slice_of_cube(pred_cube)
        target_slice = slice_of_cube(target_cube)

        return pred_slice, target_slice, pred_cube, target_cube
    
    
    def split_batch(self, pred):
        n_entries = self.inputs.shape[0]
        cube_shape = (n_entries, self.n_output_channels,
                      self.batch_size[0], self.batch_size[1], self.batch_size[2])
        pred_cube = pred.reshape(cube_shape)
        target_cube = self.targets.reshape(cube_shape)

        pred_slice = slice_of_cube(combine_cubes(pred_cube,
                                                 self.input_size, self.batch_size))
        target_slice = slice_of_cube(combine_cubes(target_cube,
                                                   self.input_size, self.batch_size))
        return pred_slice, target_slice, pred_cube, target_cube