import glob
import sys
import os
import pickle

sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

import numpy as np
import scipy.io.wavfile
from utils.plugin_feature_extractor import PluginFeatureExtractor
from tqdm import trange

def clear():
    norm_files = glob.glob("app/utils/normalisers/*")
    audio_files = glob.glob("app/data/dataset/*")
    for f in norm_files:
        os.remove(f)
    for f in audio_files:
        os.remove(f)

algorithm_number = 18
# Works:  1-15
# Bleh:  16-19
# Works: 20-32
alg = (1.0 / 32.0) * float(algorithm_number - 1) + 0.001
overriden_parameters = [(0, 1.0), (1, 0.0), (2, 1.0), (3, 0.0), (4, alg), (6,0.0),
                        (7,0.0), (8,0.0), (9,0.0), (10,0.), (11,0.0), (12,0.0),
                        (26, 1.),  (30, 0.),  (48, 1.),  (52, 0.), 
                        (70, 1.),  (74, 0.),  (92, 1.),  (96, 0.), 
                        (114, 1.), (118, 0.), (136, 1.), (140, 0.)]

# other_params = [((i + 5), 0.5) for i in range(18)]

# overriden_parameters.extend(other_params)

desired_features = [0,1,6]
desired_features.extend([i for i in range(len(desired_features), 21)])
extractor = PluginFeatureExtractor(midi_note=24, note_length_secs=4.0,
                                   desired_features=desired_features,
                                   overriden_parameters=overriden_parameters,
                                   render_length_secs=5.0,
                                   pickle_path="app/utils/normalisers",
                                   warning_mode="ignore", normalise_audio=False)

# print np.array(extractor.overriden_parameters)

path = "app/VST/Dexed.dll"
# path = "/home/tollie/Development/vsts/synths/granulator/Builds/build-granulator-Desktop-Debug/build/debug/granulator.so"
# path = "/home/tollie/Downloads/synths/FMSynth/Builds/LinuxMakefile/build/FMSynthesiser.so"

clear()

extractor.load_plugin(path)

if extractor.need_to_fit_normalisers():

    print("No normalisers found, fitting new ones.")
    extractor.fit_normalisers(100)


# Get training and testing batch.
test_size = 10
train_size = 10

operator_folder = "app/data/dataset/"


def get_batches(train_batch_size, test_batch_size, extractor):

    (f, p) = extractor.get_random_normalised_example()
    f_shape = np.array(f).shape
    train_batch_x = np.zeros((train_batch_size, f_shape[0], f_shape[1]),
                             dtype=np.float32)
    train_batch_y = np.zeros((train_batch_size, p.shape[0]), dtype=np.float32)
    for i in trange(train_batch_size, desc="Generating Train Batch"):
        (features, parameters) = extractor.get_random_normalised_example()
        train_batch_x[i] = features
        train_batch_y[i] = parameters
        audio = extractor.float_to_int_audio(extractor.get_audio_frames())
        location = operator_folder + 'train' + str(i) + '.wav'
        scipy.io.wavfile.write(location, 44100, audio)

    test_batch_x = np.zeros((test_batch_size, f_shape[0], f_shape[1]),
                            dtype=np.float32)
    test_batch_y = np.zeros((test_batch_size, p.shape[0]), dtype=np.float32)
    for i in trange(test_batch_size, desc="Generating Test Batch"):
        (features, parameters) = extractor.get_random_normalised_example()
        test_batch_x[i] = features
        test_batch_y[i] = parameters
        audio = extractor.float_to_int_audio(extractor.get_audio_frames())
        location = operator_folder + 'test' + str(i) + '.wav'
        scipy.io.wavfile.write(location, 44100, audio)

    return train_batch_x, train_batch_y, test_batch_x, test_batch_y


train_x, train_y, test_x, test_y = get_batches(train_size, test_size,
                                               extractor)
# train_x, train_y, test_x, test_y = get_spectrogram_batches(train_size,
#                                                            test_size,
#                                                            extractor)
np.save(operator_folder + "/overriden_parameters.npy", overriden_parameters)
np.save(operator_folder + "/train_x.npy", train_x)
np.save(operator_folder + "/test_x.npy", test_x)
np.save(operator_folder + "/train_y.npy", train_y)
np.save(operator_folder + "/test_y.npy", test_y)

print ("Finished.")

