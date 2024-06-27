class Converter:
    def __init__(self):
        self.patch = []

    def convertGlobals(self,voice):
            
        alg = voice.algorithm / 31
        fb = voice.feedback / 7
        lfoWave = voice.lfoWave / 5
        modSensitivityPitch = voice.pModSens / 7
        
        self.patch.append(voice.cutoff/99)
        self.patch.append(voice.resonance/99)
        self.patch.append(voice.output/99)
        self.patch.append(voice.masterTune/99)
        self.patch.append(alg)
        self.patch.append(fb)
        self.patch.append(float(voice.oscSync))
        
        for lfoParam in voice.lfo:
            self.patch.append(lfoParam/99)
        
        self.patch.append(float(voice.lfoSync))
        self.patch.append(lfoWave)
        self.patch.append(voice.middleC/127)
        self.patch.append(modSensitivityPitch)
        
        for param in voice.globalEg.rate:    
            self.patch.append(param/99)
            
        for param in voice.globalEg.level:
            self.patch.append(param/99)

    def convertOperators(self,voice):
        for i in range(len(voice.op)):
            op = voice.op[i+1]
            
            coarse = op.osc.frequency["coarse"] / 31
            detune = op.osc.detune / 14
            left_curve  = op.scaling.left_curve / 3
            right_curve  = op.scaling.right_curve / 3
            rate_scaling = op.scaling.rate / 7
            aModSens = op.sensitivity.modulation / 3
            velocity =op.sensitivity.velocity / 7
            
            for rate in op.eg.rate:
                self.patch.append(rate/99)
            
            for level in op.eg.level:
                self.patch.append(level/99)
            
            self.patch.append(op.output/99)
            self.patch.append(float(op.osc.mode))
            self.patch.append(coarse)
            self.patch.append(op.osc.frequency["fine"]/99)
            self.patch.append(detune)
            self.patch.append(op.scaling.break_point/99) # Potential error
            self.patch.append(op.scaling.left_depth/99)
            self.patch.append(op.scaling.right_depth/99)
            self.patch.append(left_curve)
            self.patch.append(right_curve)
            self.patch.append(rate_scaling)
            self.patch.append(aModSens)
            self.patch.append(velocity)
            self.patch.append(1.0)
            

    def transform_to_patch(self,voice):
        self.patch = []

        self.convertGlobals(voice.globals)
        
        if len(self.patch) != 23:
            raise Exception("Erreur: Paramètres globaux manquants")
        
        self.convertOperators(voice)
        return self.patch
            