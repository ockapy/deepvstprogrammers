import sys
import os

# Ajoute le chemin vers les modules stockés dans utils
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

import pickle
import scipy
import warnings
import numpy as np
import matplotlib.pyplot as plt
import utils.utility_functions as ult
import utils.data_set_generator as generator

from utils.sysexConverter import Converter
from utils.Create_sysex import sysex_from_patch
from models.hill_climber.hill_climber import HillClimber
from utils.plugin_feature_extractor import PluginFeatureExtractor


# Si aucun argument choisit --default
try:
    arg = sys.argv[1]
except IndexError:
    arg = "--default"
    
root = os.path.dirname(__file__)

with warnings.catch_warnings():
    operator_folder = ""
    data_folder = root+"/data/dataset/"
    
    #JPC : selectionne les features utiles, ne sert probablement à rien, mal conçu
    desired_features = [] # CF FEATURES.md
    desired_features.extend([i for i in range(0, 21)])
    
    # Partie utile uniquement en cas de génération de données d'entrainement aléatoires
    # Certains paramètres sont bloqués pour controller la génération afin de produire de manière consistente un son audible
    
        # algorithm_number = 18
        # # Works:  1-15
        # # Bleh:  16-19
        # # Works: 20-32
        # alg = (1.0 / 32.0) * float(algorithm_number - 1) + 1/64
        
        # overriden_parameters = [
        #                         # (0, 1.0), (2, 1.0), (3, 0.5), (4, alg),(5, 0.2),(6,0.0), # PARAMETRES GENERAUX
        #                         # (7,0.0), (8,0.0), (9,0.0), (10,0.), (11,0.0), (12,0.0), # PARAMETRES LFO
        #                         # (15,1.0),(16,1.0),(17,1.0), (18,1.0),(19,0.5),(20,0.5),(21,0.5),(22,0.5), # PITCH EG RATE ET LEVEL
        #                         # (29,1.0),(51,1.0),(73,1.0),(95,1.0),(117,1.0),(139,1.0), # EG 3 LEVEL
        #                         # (31,1.0), #(53,1.0),(75,1.0),(97,1.0),(119,1.0),(141,1.0), # Volume des opérateurs
        #                         ]
    
    
    
    # Met en place la liaison python RenderMan
    extractor = PluginFeatureExtractor(midi_note=60, note_length_secs=0.4,
                                   desired_features=desired_features,
                                   overriden_parameters=[],
                                   render_length_secs=0.7,
                                   pickle_path=root+"/data/normalisers",
                                   warning_mode="ignore", normalise_audio=False)
    # Chargement du VST.
    path = root+"/VST/Dexed"
    extractor.load_plugin(path)

    # Génération des normaliseurs et des données (entrainement)
    normalisers_size, test_size, iterations, samplesCount = ult.getTestSize(arg)
    generator.generateFromSysex(extractor,normalisers_size,samplesCount)

    # Training and testing batch.
    train_x = np.load(data_folder + "train_x.npy")
    train_y = np.load(data_folder + "train_y.npy")
    test_x = np.load(data_folder + "test_x.npy")
    test_y = np.load(data_folder + "test_y.npy")

    # Load models.
    features_cols = train_x[0].shape[0]
    features_rows = train_x[0].shape[1]
    parameter_size = train_y[0].shape[0]

    warnings.simplefilter("ignore")

    # Met en place le modèle
    hill_climber = HillClimber(extractor=extractor, target_features=test_x,
                               feature_size=(features_cols * features_rows),
                               parameter_size=parameter_size,
                               averaging_amount=1)

    # model_errors = {
    #     'hill_climber': [],
    # }

    # hill_prediction = hill_climber.prediction()
    # hill_climber_stats = get_stats(extractor, hill_prediction, test_x, test_y)
    # model_errors['hill_climber'] += [hill_climber_stats[0]]

    temp_best = 0
    
    # Itération sur tout les fichiers de test
    for test_file in range(1):
        print("\n************TESTING FILE N°"+str(test_file)+"*****************")

        # Fait x itérations pour chaque fichier
        for iteration in range(iterations):

            print ("\n*** Iteration: " + str(iteration) + " ***")
            
            # Ajustement des paramètres
            hill_climber.optimise(test_file)

            distance = hill_climber.get_fitness(hill_climber.current_point[test_file])
            print("\nDistance to target: "+str(distance))
            
            # Si le score est meilleur alors on fait un fichier audio avec le patch
            if (distance > temp_best):
                temp_best = distance
            
                print("\nCreating audio file")
                extractor.set_patch(hill_climber.current_point[test_file])
                audio = extractor.float_to_int_audio(extractor.get_audio_frames())
                location = root + '/data/dataset/audio/Result ' + str(round(distance,0)) + '.wav'
                scipy.io.wavfile.write(location, 48000, audio)
                
                sysex_from_patch(hill_climber.current_point[test_file])
                # sysex_loc = root + '/stats/sysex ' + str(round(distance)) + '.syx'
            
            
