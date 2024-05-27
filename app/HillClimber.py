import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
dir = os.path.dirname(__file__)

import pickle
import warnings
import matplotlib.pyplot as plt
import scipy
import numpy as np
import data_set_generator as generator

from models.hill_climber.hill_climber import HillClimber
from utils.plugin_feature_extractor import PluginFeatureExtractor
from utils.utility_functions import get_stats
from tqdm import trange

arg = sys.argv[1]


# TODO Verifier si des fichiers de test existent, si oui faire un nouveau dossier (multiple processus en même temps s'écrasent)

test_size = 0
iterations = 0
normalisers_size = 0
samplesCount = 0

if(arg == "--small"):
    normalisers_size = 100
    test_size = 10
    iterations = 1
    samplesCount = 10
elif(arg == "--medium"):
    normalisers_size = 500
    test_size = 25
    iterations = 5
    samplesCount = 25
elif(arg == "--large"):
    normalisers_size = 1000
    test_size = 50
    iterations = 10
    samplesCount = 50

# Création des répertoires necessaires pour cette expérience


with warnings.catch_warnings():
    
    
    
    # Chargement du VST.
    operator_folder = ""
    data_folder = dir+"/data/dataset/"
    
    desired_features = [] # CF FEATURES.md
    desired_features.extend([i for i in range(0, 21)])
    
    algorithm_number = 32
    # Works:  1-15
    # Bleh:  16-19
    # Works: 20-32
    alg = (1.0 / 32.0) * float(algorithm_number - 1) + 1/64
    
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
                                   pickle_path=dir+"/utils/normalisers",
                                   warning_mode="ignore", normalise_audio=False)

    path = dir+"/VST/Dexed.vst"
    extractor.load_plugin(path)
    
    generator.generate_data(extractor,normalisers_size,samplesCount)


    # Get training and testing batch.
    train_x = np.load(data_folder + "train_x.npy")
    train_y = np.load(data_folder + "train_y.npy")
    test_x = np.load(data_folder + "test_x.npy")[0:test_size]
    test_y = np.load(data_folder + "test_y.npy")[0:test_size]

    # Load models.
    features_cols = train_x[0].shape[0]
    features_rows = train_x[0].shape[1]
    parameter_size = train_y[0].shape[0]

    warnings.simplefilter("ignore")

    hill_climber = HillClimber(extractor=extractor, target_features=test_x,
                               feature_size=(features_cols * features_rows),
                               parameter_size=parameter_size,
                               averaging_amount=1)

    model_errors = {
        'hill_climber': [],
    }

    hill_prediction = hill_climber.prediction()
    hill_climber_stats = get_stats(extractor, hill_prediction, test_x, test_y)
    model_errors['hill_climber'] += [hill_climber_stats[0]]

    for iteration in range(iterations):

        print ("\n*** Iteration: " + str(iteration) + " ***")

        print("\nHill Climber: ")
        hill_climber.optimise()
        hill_prediction = hill_climber.prediction()
        hill_climber_stats = get_stats(extractor,
                                      hill_prediction,
                                      test_x,
                                      test_y)
        model_errors['hill_climber'] += [hill_climber_stats[0]]

        print ("Hill: " + str(hill_climber_stats[0]))

        print ("Start iteration " + str(iteration) + " pickling.")
        pickle.dump(hill_climber_stats, open(dir+"/stats" + operator_folder + "/hill_climber.p", "wb"))
        pickle.dump(model_errors, open(dir+"/stats" + operator_folder + "/all_hills_error.p", "wb"))
        print ("Finished iteration " + str(iteration) + " pickling.")
        print ("Finished iteration " + str(iteration) + " pickling.")
