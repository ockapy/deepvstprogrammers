import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

import pickle
import warnings
import numpy as np
import matplotlib.pyplot as plt
import data_set_generator as generator
import tensorflow.compat.v1 as tf #type: ignore
tf.disable_v2_behavior()


from ga import GeneticAlgorithm #type: ignore
from plugin_feature_extractor import PluginFeatureExtractor #type: ignore
from utility_functions import get_stats #type: ignore

# Si aucun argument choisit --small
try:
    arg = sys.argv[1]
except IndexError:
    arg = "--small"
    
root = os.path.dirname(__file__)

def setTestSize(arg):
    
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
    return normalisers_size, test_size, iterations, samplesCount



with warnings.catch_warnings():
    
    
    
    # Chargement du VST.
    operator_folder = ""
    data_folder = root+"/data/dataset/"
    
    desired_features = [] # CF FEATURES.md
    desired_features.extend([i for i in range(0, 21)])
    
    algorithm_number = 32
    # Works:  1-15
    # Bleh:  16-19
    # Works: 20-32
    alg = (1.0 / 32.0) * float(algorithm_number - 1) + 0.001
    
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
                                   pickle_path=root+"/utils/normalisers",
                                   warning_mode="ignore", normalise_audio=False)

    path = root+"/VST/Dexed.dll"
    extractor.load_plugin(path)
    
    
    normalisers_size, test_size, iterations, samplesCount = setTestSize(arg)
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
    features = tf.placeholder(tf.float32, [None, features_cols, features_rows])
    patches = tf.placeholder(tf.float32, [None, parameter_size])
    prob_keep_input = tf.placeholder(tf.float32)
    prob_keep_hidden = tf.placeholder(tf.float32)
    batch_size = tf.placeholder(tf.int32)

    warnings.simplefilter("ignore")

    ga = GeneticAlgorithm(extractor=extractor, population_size=50,
                          percent_elitism_elites=5, percent_elitist_parents=5,
                          dna_length=(parameter_size), target_features=test_x,
                          feature_size=(features_cols * features_rows),
                          mutation_rate=0.01, mutation_size=0.1)

    print ("Initialising TensorFlow variables and building tensor graph...")
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    model_errors = {
        'ga': [],
    }

    ga_prediction = ga.prediction()
    ga_stats = get_stats(extractor, ga_prediction, test_x, test_y)
    model_errors['ga'] += [ga_stats[0]]

    for iteration in range(iterations):

        print ("\n*** Iteration: " + str(iteration) + " ***")

        print ("\nGenetic Algorithm: ")
        ga.optimise()
        ga_prediction = ga.prediction()
        ga_stats = get_stats(extractor, ga_prediction, test_x, test_y)
        model_errors['ga'] += [ga_stats[0]]

        print ("Gene: " + str(ga_stats[0]))

        print ("Start iteration " + str(iteration) + " pickling.")
        pickle.dump(ga_stats, open(root +"/stats" + operator_folder + "/ga.p", "wb"))
        pickle.dump(model_errors, open(root+"/stats" + operator_folder + "/ga_models_error.p", "wb"))
        print ("Finished iteration " + str(iteration) + " pickling.")
