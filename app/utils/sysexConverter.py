class Converter:
    def __init__(self):
        self.patch = []

    def convertGlobals(self,voice):
            
        alg = (1.0 / 32.0) * float(voice.algorithm) + 1/64
        fb = (1.0 / 8.0) * float(voice.feedback) + 1/16
        lfoWave = (1.0 / 5.0) * float(voice.lfoWave) + 1/10
        modSensitivityPitch = (1.0 / 6.0) * float(voice.pModSens) + 1/12
        
        self.patch.append(voice.cutoff/100)
        self.patch.append(voice.resonance/100)
        self.patch.append(voice.output/100)
        self.patch.append(voice.masterTune/100)
        self.patch.append(alg)
        self.patch.append(fb)
        self.patch.append(float(voice.oscSync))
        
        for lfoParam in voice.lfo:
            self.patch.append(lfoParam/100)
        
        self.patch.append(float(voice.lfoSync))
        self.patch.append(lfoWave)
        self.patch.append(voice.middleC)
        self.patch.append(modSensitivityPitch)
        
        for param in voice.globalEg.rate:    
            self.patch.append(param/100)
            
        for param in voice.globalEg.level:
            self.patch.append(param/100)

    def convertOperators(self,voice):
        for i in range(len(voice.op)):
            op = voice.op[i+1]
            
            coarse = (1.0 / 32.0) * float(op.osc.frequency["coarse"]) + 1/64
            detune = (1.0 / 15.0) * float(op.osc.detune) + 1/30
            left_curve  = (1.0 / 4.0) * float(op.scaling.left_curve) + 1/8
            right_curve  = (1.0 / 4.0) * float(op.scaling.right_curve) + 1/8
            rate_scaling = (1.0 / 8.0) * float(op.scaling.rate) + 1/16
            aModSens = (1.0 / 4.0) * float(op.sensitivity.modulation) + 1/8
            velocity = (1.0 / 8.0) * float(op.sensitivity.velocity) + 1/16
            
            for rate in op.eg.rate:
                self.patch.append(rate/100)
            
            for level in op.eg.level:
                self.patch.append(level/100)
            
            self.patch.append(op.output/100)
            self.patch.append(float(op.osc.mode))
            self.patch.append(coarse)
            self.patch.append(op.osc.frequency["fine"]/100)
            self.patch.append(detune)
            self.patch.append(op.scaling.break_point/100)
            self.patch.append(op.scaling.left_depth/100)
            self.patch.append(op.scaling.right_depth/100)
            self.patch.append(left_curve)
            self.patch.append(right_curve)
            self.patch.append(rate_scaling)
            self.patch.append(aModSens)
            self.patch.append(velocity)
            self.patch.append(1.0)
            

    def transform_to_patch(self,voice):
        self.convertGlobals(voice.globals)
        
        if len(self.patch) != 23:
            raise Exception("Erreur: Paramètres globaux manquants")
        
        self.convertOperators(voice)
        return self.patch
            