import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
import pickle
import warnings
import numpy as np
import data_set_generator as generator
from models import mlp_torch
from plugin_feature_extractor import PluginFeatureExtractor
from utility_functions import get_stats
import matplotlib.pyplot as plt
import torch


arg = sys.argv[1]

test_size = 0
train_size = 0
iterations = 0
normalisers_size = 0
samplesCount = 0

if(arg == "--small"):
    normalisers_size = 100
    test_size = 16
    train_size = 32
    iterations = 15
elif(arg == "--medium"):
    normalisers_size = 500
    test_size = 25
    train_size = 25
    iterations = 5
    samplesCount = 25
elif(arg == "--large"):
    normalisers_size = 1000
    test_size = 50
    train_size = 50
    iterations = 10
    samplesCount = 50

def generateSmple():
 # Chargement du VST.
    data_folder = os.path.dirname(__file__)+"/data/dataset/"
    
    desired_features = []
    desired_features.extend([i for i in range(0, 21)])
    
    algorithm_number = 32
    alg = (1.0/32.0) * float (algorithm_number-1) + 1/64
    
    overriden_parameters = [(0, 1.0), (2, 1.0), (3, 0.5), (4, alg),(5, 0.2),(6,0.0), # PARAMETRES GENERAUX
                        (7,0.0), (8,0.0), (9,0.0), (10,0.), (11,0.0), (12,0.0), # PARAMETRES LFO
                        (15,1.0),(16,1.0),(17,1.0), (18,1.0),(19,0.5),(20,0.5),(21,0.5),(22,0.5), # PITCH EG RATE ET LEVEL
                        (29,1.0),(51,1.0),(73,1.0),(95,1.0),(117,1.0),(139,1.0), # EG 3 LEVEL
                        (31,1.0), #(53,1.0),(75,1.0),(97,1.0),(119,1.0),(141,1.0), # Volume des opérateurs
                        (26, 1.0),  (30, 0.0),  (48, 1.0),  (52, 0.0),  # ASSURE QUE CHAQUE NOTE SE TERMINE (EG 4 rate et level)
                        (70, 1.0),  (74, 0.0),  (92, 1.0),  (96, 0.0), 
                        (114, 1.0), (118, 0.0), (136, 1.0), (140, 0.0)]
    
    extractor = PluginFeatureExtractor(midi_note=24, note_length_secs=0.4,
                                       desired_features=desired_features,
                                       overriden_parameters=overriden_parameters,
                                       render_length_secs=0.4,
                                       pickle_path=os.path.dirname(__file__)+"/data/normalisers",
                                       warning_mode="ignore",normalize_audio=False)
    
    path = os.path.dirname(__file__)+"/VST/Dexed.dll"
    extractor.load_plugin(path)
    generator.generate_data(extractor,normalisers_size,samplesCount)
    

    train_x = np.load(data_folder + "train_x.npy")
    train_y = np.load(data_folder + "train_y.npy")
    test_x = np.load(data_folder + "test_x.npy")[0:test_size]
    test_y = np.load(data_folder + "test_y.npy")[0:test_size]

    # Load models.
    features_cols = train_x[0].shape[0]
    features_rows = train_x[0].shape[1]
    parameter_size = train_y[0].shape[0]
    
with warnings.catch_warnings():

    warnings.simplefilter("ignore")

    # Création de l'instance
    model = mlp_torch.LinearModel(40,155)

    # Test avec création d'un tenseur d'entrée avec un batch de 10
    batchSize = 10
    X = torch.rand(batchSize,40)

    # Passe à travers du modèle le premier vecteur
    Y = model(X[0])