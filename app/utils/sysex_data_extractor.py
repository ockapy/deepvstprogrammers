import numpy as np
from enum import Enum
from sysexConverter import Converter

class SX(Enum):
    start = 0xF0
    end = 0xF7
    yamaha = 0x43

def uint14(b1,b2):
    return (b1 << 7)+b2

def cheksum7(array):
    somme = sum(array)
    inv = (~somme)+1
    return inv & 0x7F

class DX7eg:
    def __init__(self,data):
        self._analyse(data)

    def _analyse(self,data):
        if (len(data) != 8):
           raise Exception("wrong Envelope Generator size : "+data.length);

        self.rate = [data[i] for i in range(4)]


        self.level = [data[i+4] for i in range(4)]
        for i in range(4):
            self.level[i] = data[i+4]
       
class DX7scaling:
    def __init__(self,data):
        self._analyse(data)

    def _analyse(self,data):
        if (len(data) != 6):
            raise Exception("Wrong scaling size")
        
        self.break_point = data[0]
        self.left_depth = data[1]
        self.right_depth = data[2]
        self.left_curve = data[3]
        self.right_curve  = data[4]
        self.rate = data[5]
              
class DX7sensitivity:
    def __init__(self,data):
        self._analyse(data)

    def _analyse(self,data):
        if (len(data) != 2):
           raise Exception("wrong sensivity size : "+data.length);

        self.modulation = data[0]
        self.velocity = data[1]

class DX7osc:
    def __init__(self,data):
        self._analyse(data)

    def _analyse(self,data):
        if (len(data) != 4):
           raise Exception("wrong oscillator size : "+data.length);

        self.mode = data[0]
        self.frequency = {
            "coarse": data[1],
            "fine": data[2]
        }
        self.detune = data[3]

class DX7op:
    
    def __init__(self,data):
        self._analyse(data)
        
    def _analyse(self,data):
        if(len(data)!=21):
            raise Exception("Wrong operator size")
        
        self.eg = DX7eg(data[0:8])
        self.scaling = DX7scaling(data[8:14])
        self.sensitivity = DX7sensitivity(data[14:16])
        self.output=data[16]
        self.osc = DX7osc(data[17:21])

class DX7globals:
    def __init__(self,data):
        self._analyse(data)
        self.cutoff = 99
        self.resonance = 0
        self.output = 99
        self.masterTune = 50
        self.middleC = 24


    def _analyse(self,data):

        self.algorithm = data[8]
        self.feedback = data[9]
        self.oscSync = data[10]

        self.lfo = [data[i+11] for i in range(4)]

        self.lfoSync = data[15]
        self.lfoWave = data[16]
        self.pModSens = data[17]
        self.globalEg = DX7eg(data[0:8])
        
class DX7voice:
    
    def __init__(self,data):
        self._analyse(data)
        
    def _analyse(self,data):
        if(len(data)!=155):
            raise Exception("Wrong voice size")
        
        self.op = {}
        pos = 0
        for i in range(6,0,-1):
            self.op[i]= DX7op(data[pos:pos+21])
            pos+=21
        
        self.globals = DX7globals(data[126:145])
        
        self.name = data[145:155].tobytes().decode('utf-8')

class DX7:
    def __init__(self,data):
        self.voice = None
        self._analyse(data)
    
    def _analyse(self,data):
        # if('byteLength' not in data):
        #     raise TypeError("Wrong type: byteLength expected")
            
        if(len(data) != 163):
            raise Exception("Size should be of 163")
        
        sx = np.frombuffer(data,dtype=np.uint8)
        
        if(sx[0] != SX.start.value or sx[1] != SX.yamaha.value):
            raise Exception("Wrong sysex header")
        
        if(sx[3] != 0):
            raise Exception("Wrong sysex format: voice expected")
        
        datasize = uint14(sx[4],sx[5])
        voiceSize = 155
        if (datasize!=voiceSize):
            raise Exception("Wrong sysex data size")
        
        voice = sx[6:voiceSize+6]
        
        checksum = cheksum7(voice)
        sxsk = sx[voiceSize+6]
        if(sxsk != checksum):
            raise Exception("Wrong sysex checksum")
        
        if(sx[voiceSize+7] != SX.end.value):
            raise Exception("Wrong sysex end")
        
        self.voice = DX7voice(voice)
           
                
            
with open('../data/Chicago2.syx',"rb") as file:
    data = file.read()
    dx7 = DX7(data)
    
    converter = Converter()
    
    
    patch = converter.transform_to_patch(voice=dx7.voice)
    
    print("finished")