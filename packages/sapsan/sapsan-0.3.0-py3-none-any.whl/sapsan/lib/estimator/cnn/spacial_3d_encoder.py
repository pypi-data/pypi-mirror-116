"""
Spacial 3d encoder estimator

    - uses pytorch_estimator for backend

For example see sapsan/examples/cnn_example.ipynb
"""
import json
import numpy as np

import torch

from sapsan.core.models import EstimatorConfig
from sapsan.lib.estimator.pytorch_estimator import TorchEstimator
from sapsan.lib.data import get_loader_shape


class CNN3dModel(torch.nn.ModuleDict):
    def __init__(self, D_in = 1, D_out = 1):
        super(CNN3dModel, self).__init__()
        
        self.conv3d = torch.nn.Conv3d(D_in, D_in*2, kernel_size=2, stride=2, padding=1)
        self.conv3d2 = torch.nn.Conv3d(D_in*2, D_in*2, kernel_size=2, stride=2, padding=1)
        self.conv3d3 = torch.nn.Conv3d(D_in*2, D_in*4, kernel_size=2, stride=2, padding=1)
        self.pool = torch.nn.MaxPool3d(kernel_size=2, padding=1)
        self.pool2 = torch.nn.MaxPool3d(kernel_size=2) #kernel_size=2 for 64^3

        self.relu = torch.nn.ReLU()

        self.linear = torch.nn.Linear(D_in*4, D_in*8)
        self.linear2 = torch.nn.Linear(D_in*8, D_out)

    def forward(self, x): 

        x = x.float()
        c1 = self.conv3d(x)
        p1 = self.pool(c1)
        c2 = self.conv3d2(self.relu(p1))
        p2 = self.pool(c2)
        c3 = self.conv3d3(self.relu(p2))
        p3 = self.pool2(c3)

        v1 = p3.view(p3.size(0), -1)  
        
        l1 = self.relu(self.linear(v1))
        l2 = self.linear2(l1)   

        return l2

    
class CNN3dConfig(EstimatorConfig):
    def __init__(self,
                 n_epochs: int = 1,
                 patience: int = 10,
                 min_delta: float = 1e-5, 
                 logdir: str = "./logs/",
                 *args, **kwargs):
        self.n_epochs = n_epochs
        self.logdir = logdir
        self.patience = patience
        self.min_delta = min_delta
        self.kwargs = kwargs
        
        #everything in self.parameters will get recorded by MLflow
        self.parameters = {
                        "model - n_epochs": self.n_epochs,
                        "model - min_delta": self.min_delta,
                        "model - patience": self.patience,
                    }       
    
    
class CNN3d(TorchEstimator):
    def __init__(self, config = CNN3dConfig(), 
                       model = CNN3dModel()):
        super().__init__(config, model)
        self.config = config

    def train(self, loaders):

        x_shape, y_shape = get_loader_shape(loaders)
        model = CNN3dModel(x_shape[1], y_shape[1])
        
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        loss_func = torch.nn.MSELoss()  # torch.nn.SmoothL1Loss()
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,
                                                               patience=self.config.patience,
                                                               min_lr=1e-5) 
        
        trained_model = self.torch_train(loaders, model, 
                                         optimizer, loss_func, scheduler, 
                                         self.config)
                
        return trained_model