import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../lazyloadingutils'))
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# Sous classe de Module
class LinearModel(nn.Module):
    def __init__(self,in_features,out_features):
        super().__init__()
        # Première couche en entrée : le nombre de paramètre d'un 
        self.l1 = nn.Linear(in_features, out_features)
    def forward(self, x):
        return self.l1(x)


