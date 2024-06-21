import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

import glob
import numpy as np
import scipy.io.wavfile
import sysex_data_extractor as sd
from tqdm import trange

root = os.path.dirname(os.path.dirname(__file__))

# Remove normalisers and audio files before start a new data generation.
def clear():
    norm_files = glob.glob(root+"/data/normalisers/*")
    audio_files = glob.glob(root+"/data/dataset/audio/*")
    for f in norm_files:
        os.remove(f)
    for f in audio_files:
        os.remove(f)


def get_batches(train_batch_size, test_batch_size, extractor,operator_folder):

    (frames, patch) = extractor.get_random_normalised_example()
    f_shape = np.array(frames).shape
    train_batch_x = np.zeros((train_batch_size, f_shape[0], f_shape[1]),
                             dtype=np.float32)
    train_batch_y = np.zeros((train_batch_size, patch.shape[0]), dtype=np.float32)
    for i in trange(train_batch_size, desc="Generating Train Batch"):
        (frames, patch) = extractor.get_random_normalised_example()
        train_batch_x[i] = frames
        train_batch_y[i] = patch
        audio = extractor.float_to_int_audio(extractor.get_audio_frames())
        location = operator_folder + '/audio/train' + str(i) + '.wav'
        scipy.io.wavfile.write(location, 48000, audio)


    test_batch_x = np.zeros((test_batch_size, f_shape[0], f_shape[1]),
                            dtype=np.float32)
    test_batch_y = np.zeros((test_batch_size, patch.shape[0]), dtype=np.float32)
    for i in trange(test_batch_size, desc="Generating Test Batch"):
        (features, parameters) = extractor.get_random_normalised_example()
        test_batch_x[i] = features
        test_batch_y[i] = parameters
        audio = extractor.float_to_int_audio(extractor.get_audio_frames())
        location = operator_folder + '/audio/test' + str(i) + '.wav'
        scipy.io.wavfile.write(location, 48000, audio)

    return train_batch_x, train_batch_y, test_batch_x, test_batch_y


def checkfolders():
    if not os.path.exists(root+"/data/dataset/audio/"):
        os.makedirs(root+"/data/dataset/audio/")
    if not os.path.exists(root+"/stats/"):
        os.makedirs(root+"/stats/")

def generate_data(extractor,size,samplesCount):
    
    checkfolders()
    
    clear()
    
    if extractor.need_to_fit_normalisers():
        print("No normalisers found, fitting new ones.")
        extractor.fit_normalisers(size)

    # Get training and testing batch.
    test_size = samplesCount
    train_size = samplesCount

    operator_folder = root+"/data/dataset/"

    train_x, train_y, test_x, test_y = get_batches(train_size, test_size, extractor,operator_folder)
    
    # train_x, train_y, test_x, test_y = get_spectrogram_batches(train_size,
    #                                                            test_size,
    #                                                            extractor)
    
    np.save(operator_folder + "/overriden_parameters.npy", extractor.overriden_parameters)
    np.save(operator_folder + "/train_x.npy", train_x)
    np.save(operator_folder + "/test_x.npy", test_x)
    np.save(operator_folder + "/train_y.npy", train_y)
    np.save(operator_folder + "/test_y.npy", test_y)

    print ("Finished.")
    
    return True

def generateFromSysex(extractor):
    
    checkfolders()
    
    clear()
    
    operator_folder = root+"/data/dataset/"

    
    bank = sd.getVoice(root+"/VST/SynprezFM_01.syx")
    
    patches = sd.bankToPatches(bank)
    count=1
    for patch in patches:
        extractor.set_patch(patch)
        audio = extractor.float_to_int_audio(extractor.get_audio_frames())
        location = operator_folder + '/audio/song' + str(count) + '.wav'
        scipy.io.wavfile.write(location, 48000, audio)
        count+=1
    print ("Finished.")
    
    return True

