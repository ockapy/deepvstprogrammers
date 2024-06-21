import os

import joblib
import warnings

import numpy as np
import librenderman as rm

from tqdm import trange
from PluginPatch import PluginPatch
from sklearn import preprocessing
from pyAudioAnalysis import ShortTermFeatures as fe
import sys

class PluginFeatureExtractor:

    def __init__(self, **kwargs):
        self.sample_rate = kwargs.get('sample_rate', 48000)
        self.buffer_size = kwargs.get('buffer_size', 512)
        self.midi_note = kwargs.get('midi_note', 40)
        self.midi_velocity = kwargs.get('midi_velocity', 127)
        self.note_length_secs = kwargs.get('note_length_secs', 1.0)
        self.render_length_secs = kwargs.get('render_length_secs', 2.5)
        self.frame_step_ms = kwargs.get('frame_step_ms', 25)
        self.frame_size_ms = kwargs.get('frame_size_ms', 50)
        self.pickle_path = kwargs.get('pickle_path', "")
        self.overriden_parameters = kwargs.get('overriden_parameters', [])
        if len(self.overriden_parameters) > 0:
            self.overriden_parameters.sort(key=lambda tup: tup[0])
        self.warning_mode = kwargs.get('warning_mode', "always")
        self.normalise_audio = kwargs.get('normalise_audio', False)
        self.desired_features_indices = kwargs.get('desired_features', [i for i in range(21)])
        self.frame_size_samples = int(self.frame_size_ms * self.sample_rate / 1000.0)
        self.frame_step_samples = int(self.frame_step_ms * self.sample_rate / 1000.0)
        self.loaded_plugin = False
        self.rendered_patch = False
        self.parameter_size = None
        self.plugin_patch = PluginPatch()


    def load_plugin(self, plugin_path):
        self.engine = rm.RenderEngine(self.sample_rate, self.buffer_size, 2048)
        if plugin_path == "":
            print ("Please supply a non-empty path")
            return False
    
        if sys.platform == 'win32':
            plugin_path += ".dll"
        elif sys.platform == 'darwin':
            plugin_path += ".vst"
        else:
            raise Exception("Unsupported operating system")
        
        if(self.engine.load_plugin(plugin_path)):
            self.plugin_patch.set_parameters_name(self.engine.get_plugin_parameters_description())

            self.loaded_plugin = True
            self.generator = rm.PatchGenerator(self.engine)

            self.plugin_patch.initiate_patch(self.generator.get_random_patch(),self.overriden_parameters)

            print ("Successfully loaded plugin.")
            return True
        else:
            raise Exception("Unsuccessful loading of plugin: is the path correct?")


    def set_patch(self, patch):
        if self.loaded_plugin:
            self.engine.set_patch(self.plugin_patch.to_list())
            # self.engine.set_patch(plugin_patch)
            self.engine.render_patch(self.midi_note,
                                     self.midi_velocity,
                                     self.note_length_secs,
                                     self.render_length_secs)
            self.rendered_patch = True
            return True
        else:
            print ("Please load plugin first")

    def get_features_from_patch(self, patch):
        if self.pickle_files_exist():
            files = self.get_file_paths()
            if self.set_patch(patch):
                int_audio_frames = self.float_to_int_audio(np.array(self.get_audio_frames()))
                feature_vector = self.get_desired_features(int_audio_frames)
                contains_nan = np.isnan(feature_vector).any()
                if contains_nan:
                    feature_vector = np.zeros_like(feature_vector)
                normalisers = [joblib.load(files[i]) for i in range(len(files))]
                index = 0
                for i in range(len(normalisers)):
                    if i in self.desired_features_indices:
                        normalised_features=(normalisers[i].transform(feature_vector))
                        index += 1
                norm_features = np.array(normalised_features)
                return norm_features.T
            else:
                return None
        else:
            print ("Please train normalisers using PluginFeatureExtractor.fit_normalisers().")

    # def add_patch_indices(self, patch : Patch):
    #     tuple_patch = []
    #     for i in range(len(patch)):
    #         tuple_patch += [(i, float(patch[i]))]
    #     return tuple_patch

    # def remove_patch_indices(self, patch):
    #     return np.array([parameter[1] for parameter in patch])

    # def list_patch(self):
    #     lines = self.engine.get_plugin_parameters_description()
    #     if self.patch == None:
    #         print (lines)
    #     else:
    #         lines = lines.split('\n')
    #         lines_with_values = []
    #         print ( len(lines) )
    #         for i, ln in enumerate(lines):
    #             if ln != "":
    #                 value = self.patch[i]
    #                 line = '{0: <22}'.format(ln) + "(" + str(value) + ")"
    #                 lines_with_values.append(line)
    #         print ("\n".join(str(x) for x in lines_with_values))

    def get_audio_frames(self):
        if self.rendered_patch:
            audio = np.array(self.engine.get_audio_frames())
            if self.normalise_audio:
                return audio / np.max(np.abs(audio), axis=0)
            return audio
        else:
            print ("Please set and render a patch before trying to get audio frames.")

    # def write_to_wav(self, path):
    #     if self.rendered_patch:
    #         float_audio = np.array(self.get_audio_frames())
    #         int_audio = self.float_to_int_audio(float_audio)
    #         scipy.io.wavfile.write(path, 44100, int_audio)
    #     else:
    #         print ("Render a patch first before writing to file!")

    def float_to_int_audio(self, float_audio_frames):
        float_audio_frames *= 32768
        return np.clip(float_audio_frames, -32768, 32767).astype(np.int16)

    def  get_random_example(self): # TODO WIP
        if self.loaded_plugin:
            while True:
                
                self.plugin_patch.randomise()
                self.plugin_patch.override_parameters()
                
                self.set_patch(self.plugin_patch.patch)
                
                # random_patch_list_tuples = self.generator.get_random_patch() # TO SLOW
                # random_patch = np.array([p[1] for p in random_patch_list_tuples])
                # random_patch = self.patch_to_partial_patch(random_patch)
                # self.set_patch(random_patch_list_tuples)
                
                int_audio_frames = self.float_to_int_audio(np.array(self.get_audio_frames()))
                feature_vector = self.get_desired_features(int_audio_frames)
                    
                return (feature_vector.T)
        else:
            print ("Please load plugin first.")
            
            

    # TODO incohérence, pourquoi récupérer les features que l'on souhaite si on est forcés de toutes les prendres au départ ???
    def get_desired_features(self, int_audio_frames):
        feature_vector, feature_names = fe.feature_extraction(int_audio_frames,
                                                self.sample_rate,
                                                self.frame_size_samples,
                                                self.frame_step_samples, deltas=False,) # Ne calcule pas les deltas, deux fois moins d'operations pour le même résultat
        output = []
        for desired_index in self.desired_features_indices:
            output.append(feature_vector[desired_index])
        return np.array(output)

    def get_file_paths(self):
        if not self.pickle_path.endswith('/') and self.pickle_path != "":
            self.pickle_path += "/"
        files = [self.pickle_path + "zero_crossing_rate.pkl",
                 self.pickle_path + "energy.pkl",
                 self.pickle_path + "energy_entropy.pkl",
                 self.pickle_path + "spectral_centroid.pkl",
                 self.pickle_path + "spectral_spread.pkl",
                 self.pickle_path + "spectral_entropy.pkl",
                 self.pickle_path + "spectral_flux.pkl",            # TODO FEATURES
                 self.pickle_path + "spectral_rolloff.pkl",
                 self.pickle_path + "mfccs0.pkl",
                 self.pickle_path + "mfccs1.pkl",
                 self.pickle_path + "mfccs2.pkl",
                 self.pickle_path + "mfccs3.pkl",
                 self.pickle_path + "mfccs4.pkl",
                 self.pickle_path + "mfccs5.pkl",
                 self.pickle_path + "mfccs6.pkl",
                 self.pickle_path + "mfccs7.pkl",
                 self.pickle_path + "mfccs8.pkl",
                 self.pickle_path + "mfccs9.pkl",
                 self.pickle_path + "mfccs10.pkl",
                 self.pickle_path + "mfccs11.pkl",
                 self.pickle_path + "mfccs12.pkl"]
        return files

    def pickle_files_exist(self):
        def files_exist(file_paths):
            for file_path in file_paths:
                if not file_path or not os.path.isfile(file_path):
                    return False
            return True
        files = self.get_file_paths()
        return files_exist(files)

    def need_to_fit_normalisers(self):
        return not self.pickle_files_exist()

    def get_random_normalised_example(self):
        with warnings.catch_warnings():
            warnings.simplefilter(self.warning_mode)
            if self.pickle_files_exist():
                files = self.get_file_paths()
                normalisers = [joblib.load(files[i]) for i in range(len(files))]

                features = self.get_random_example()
                
                patch = np.array(list(self.plugin_patch.patch.values()),dtype=np.float32)
            
                index = 0
                for i in range(len(normalisers)):
                    if i in self.desired_features_indices:
                        normalised_features= normalisers[i].transform(features.T)
                        index += 1

                norm_features = np.array(normalised_features)

                assert norm_features.T.shape == features.shape
                return (norm_features.T, patch)
            else:
                print ("Please train normalisers using PluginFeatureExtractor.fit_normalisers().")

    def fit_normalisers(self, amount):
        # if len(self.desired_features_indices) != 21:
        #     print ("Please set the feature extractor to extract all available features!") # peut être ne pas demander à l'utilisateur les features souhaitées
        #     return
        with warnings.catch_warnings():
            warnings.simplefilter(self.warning_mode)
            path = os.path.dirname(os.path.dirname(__file__)) + "/data/" + self.pickle_path
            print ("\nBeginning to fit normalisers in " + path)
            f = self.get_random_example()
            (y, x) = f.shape

            # Get the features for fitting and reshape them.
            all_features = np.empty([amount, y, x])
            for i in trange(amount, desc="Rendering Examples"):
                features = self.get_random_example()
                all_features[i] = features
            all_features = np.reshape(all_features, (x, amount, y))

            # Create the normalisers and fit them using the data.
            normalisers = [preprocessing.MinMaxScaler() for i in range(x)]
            for i in trange(x, desc="Fitting normalisers"):
                normalisers[i].fit_transform(all_features[i])
                
            # Pickle the normalisers for future sessions.
            pickle_paths = self.get_file_paths()
            for i in range(x):
                if not os.path.exists(self.pickle_path):
                    os.makedirs(self.pickle_path)

                joblib.dump(normalisers[i], pickle_paths[i])

    def overrideParameters(self,parameters):
        for(index,value) in self.overriden_parameters:
            parameters[index] = value
        return parameters