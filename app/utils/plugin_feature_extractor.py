import os
import sys

import joblib
import warnings

import numpy as np
import librenderman as rm

from tqdm import trange
from PluginPatch import PluginPatch
from sklearn import preprocessing
from pyAudioAnalysis import ShortTermFeatures as fe

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

    # Charge un plugin dans RenderMan
    def load_plugin(self, plugin_path):
        self.engine = rm.RenderEngine(self.sample_rate, self.buffer_size, 2048)
        if plugin_path == "":
            print ("Please supply a non-empty path")
            return False
    
        # Charge la bonne version d'un vst selon l'OS
        if sys.platform == 'win32':
            plugin_path += ".dll"
        elif sys.platform == 'darwin':
            plugin_path += ".vst"
        else:
            raise Exception("Unsupported operating system")
        
        # Vérifie si RenderMan charge bien le plugin
        if(self.engine.load_plugin(plugin_path)):
            
            # Récupère le nom de chaque paramètre pour le mettre dans le pluginPatch
            self.plugin_patch.set_parameters_name(self.engine.get_plugin_parameters_description())
            self.loaded_plugin = True
            
            # Initalise le générateur de patchs de RenderMan
            self.generator = rm.PatchGenerator(self.engine)

            # Créé un patch aléatoire et ajoute les paramètres bloqués dans le plugin Patch
            self.plugin_patch.initiate_patch(self.generator.get_random_patch(),self.overriden_parameters)

            print ("Successfully loaded plugin.")
            print ("Parameter count: " + str(len(self.plugin_patch.patch)))
            return True
        else:
            raise Exception("Unsuccessful loading of plugin: is the path correct?")

    # Charge un patch dans RenderMan
    def set_patch(self, patch):
        if self.loaded_plugin:
            
            # Met à jour les valeurs du plugin patch
            self.plugin_patch.update_values(patch)
            self.engine.set_patch(self.plugin_patch.to_list())
            
            self.engine.render_patch(self.midi_note,
                                     self.midi_velocity,
                                     self.note_length_secs,
                                     self.render_length_secs)
            
            self.rendered_patch = True
            return True
        else:
            print ("Please load plugin first")

    # Récupère depuis un patch les features audio du son produit
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
                
               
                normalised_features=normalisers[0].transform(feature_vector)

                # for i in range(len(normalisers)):
                #     if i in self.desired_features_indices:
                #         normalised_features=(normalisers[i].transform(feature_vector)) # Pas de sens car tout les transformations donnent le même résultat...
                #         index += 1
                        
                norm_features = np.array(normalised_features)
                return norm_features.T
            else:
                return None
        else:
            print ("Please train normalisers using PluginFeatureExtractor.fit_normalisers().")

    # Récupère les audio frames du patch chargé
    def get_audio_frames(self):
        if self.rendered_patch:
            audio = np.array(self.engine.get_audio_frames())
            if self.normalise_audio:
                return audio / np.max(np.abs(audio), axis=0)
            return audio
        else:
            print ("Please set and render a patch before trying to get audio frames.")

    # Passe les valeurs des audio frames en int
    def float_to_int_audio(self, float_audio_frames):
        float_audio_frames *= 32768
        return np.clip(float_audio_frames, -32768, 32767).astype(np.int16)

    # Randomise les valeurs du patch actuel 
    def  get_random_example(self): # TODO WIP
        if self.loaded_plugin:
            while True:
                
                self.plugin_patch.randomise()
                self.plugin_patch.override_parameters()
                
                self.set_patch(self.plugin_patch.patch)
                
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
        # output = []
        # for desired_index in self.desired_features_indices:
        #     output.append(feature_vector[desired_index])
        # return np.array(output)
        return np.array(feature_vector[0:21])

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

    # Renvoie des features normalisées et leur patch associé
    def get_random_normalised_example(self):
        with warnings.catch_warnings():
            warnings.simplefilter(self.warning_mode)
            if self.pickle_files_exist():
                files = self.get_file_paths()
                normalisers = [joblib.load(files[i]) for i in range(len(files))]

                features = self.get_random_example()
                
                patch = np.array(list(self.plugin_patch.patch.values()),dtype=np.float32)
            
                for i in range(len(normalisers)):
                    if i in self.desired_features_indices:
                        normalised_features= normalisers[i].transform(features.T)
     
                norm_features = np.array(normalised_features)

                assert norm_features.T.shape == features.shape
                return (norm_features.T, patch)
            else:
                print ("Please train normalisers using PluginFeatureExtractor.fit_normalisers().")
                
    def dataset_from_sysex(self,patch):
        with warnings.catch_warnings():
            warnings.simplefilter(self.warning_mode)
            if self.pickle_files_exist():
                files = self.get_file_paths()
                normalisers = [joblib.load(files[i]) for i in range(len(files))]
                
                self.set_patch(patch)
                patch = np.array(list(self.plugin_patch.patch.values()),dtype=np.float32)
                
                int_audio_frames = self.float_to_int_audio(np.array(self.get_audio_frames()))
                feature_vector = self.get_desired_features(int_audio_frames)
                
                for i in range(len(normalisers)):
                    if i in self.desired_features_indices:
                        normalised_features= normalisers[i].transform(feature_vector)
                        
                norm_features = np.array(normalised_features)
              
                assert norm_features.shape == feature_vector.shape
                return (norm_features.T, patch)  
                    

    def fit_normalisers(self, amount):
        with warnings.catch_warnings():
            warnings.simplefilter(self.warning_mode)
            path = os.path.dirname(os.path.dirname(__file__)) + "/data/" + self.pickle_path
            print ("\nBeginning to fit normalisers in " + path)

            # Get the features for fitting and reshape them.
            f = self.get_random_example()
            (y, x) = f.shape
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
