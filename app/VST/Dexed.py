class Dexed:
    def __init__(self):
        self.operators = {
            "op1": [],
            "op2": [],
            "op3": [],
            "op4": [],
            "op5": [],
            "op6": []
        }
        self.tune = 0
        self.cutoff = 0
        self.resonance = 0
        self.master = 0
        self.transpose = 0
        self.monophonic = 0
        self.algorithm = 0
        self.feedback = 0
        self.waveform = 0
        self.PMS = 0
        self.speed = 0
        self.delay = 0
        self.PMD = 0
        self.AMD = 0
        self.LFOKeySync = 0
        self.OSCKeySync = 0
        self.pitchEgLevel = [0,0,0,0]
        self.pitchEgRate = [0,0,0,0]

    def setOperator(self, operator, parameters):

        if (operator not in self.operators):
            raise Exception("Invalid operator")

        if (len(parameters) != 22):
            raise Exception("Operator must contain 22 parameters")
        self.operators[operator] = parameters
        