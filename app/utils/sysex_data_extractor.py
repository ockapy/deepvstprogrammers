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
        self._decodeEG(data)       

    def _decodeEG(self,data):
        if (len(data) != 8):
           raise Exception("wrong Envelope Generator size : "+data.length);

        self.rate = [data[i] for i in range(4)]


        self.level = [data[i+4] for i in range(4)]
        for i in range(4):
            self.level[i] = data[i+4]

class DX7scaling:
    def __init__(self,data,bank=False):
        if bank:
            self._decodeVMEM(data)
        else:
            self._decodeVCED(data)

    def _decodeVCED(self,data):
        if len(data) != 6:
            raise Exception("Wrong scaling size")
        
        self.break_point = data[0]
        self.left_depth = data[1]
        self.right_depth = data[2]
        self.left_curve = data[3]
        self.right_curve  = data[4]
        self.rate = data[5]
    
    def _decodeVMEM(self,data):
        
        if len(data) != 5:
            raise Exception("Wrong scaling size")
                
        self.break_point = data[0]
        self.left_depth = data[1]
        self.right_depth = data[2]
        self.left_curve = data[3] & 3
        self.right_curve = ((data[3] << 2) & 3)
        self.rate = data[4] & 7  
                     
class DX7sensitivity:
    def __init__(self,data,bank=False):
        
        if bank:
            self._decodeVMEM(data)
        else:
            self._decodeVCED(data)
            
    def _decodeVCED(self,data):
        if (len(data) != 2):
            raise Exception("wrong sensivity size : "+data.length);
        
        self.modulation = data[0]
        self.velocity = data[1]
 
    def _decodeVMEM(self,data):  
        self.modulation = data & 3
        self.velocity = (data >> 2) & 7
           
class DX7osc:
    def __init__(self,data,data2=[],bank=False):
           
        if bank:
            self._decodeVMEM(data,data2)
        else:
            self._decodeVCED(data)
        
    def _decodeVCED(self,data): 
        if (len(data) != 4):
            raise Exception("wrong oscillator size : "+data.length);

        self.mode = data[0]
        self.frequency = {
            "coarse": data[1],
            "fine": data[2]
        }
        self.detune = data[3]
        
        
    def _decodeVMEM(self,data,data2):
        if (len(data2) != 2) and (len(data)!=1):
            raise Exception("Wrong oscillator size")
        
        self.mode = data2[0] & 1
        self.frequency = {
            "coarse": (data2[0] >> 1) & 5,
            "fine": data2[1]
        }  
        self.detune = (data >> 3) & 0xF        
            
                
    

class DX7op:
    
    def __init__(self,data,bank=False):
        
        self.eg = DX7eg(data[0:8])
        
        if bank:
            self._decodeVMEM(data)
        else:
            self._decodeVCED(data)
        
    def _decodeVCED(self,data):
        if len(data) != 21:
            raise Exception("Wrong operator size")

        self.scaling = DX7scaling(data[8:14])
        self.sensitivity = DX7sensitivity(data[14:16])
        self.output=data[16]
        self.osc = DX7osc(data[17:21])        
             
    def _decodeVMEM(self,data):

        if len(data) != 17:
            raise Exception("Wrong operator size")
        
        self.scaling = DX7scaling(data[8:13],True)
        self.osc = DX7osc(data[12],data[15:17],True)
        self.sensitivity = DX7sensitivity(data[13],True)
        self.output=data[14]

            
        
        
        
        

class DX7globals:
    def __init__(self,data,bank=False):
        self.cutoff = 99
        self.resonance = 0
        self.output = 99
        self.masterTune = 50
        self.middleC = 24
        self.globalEg = DX7eg(data[0:8])
        
        if bank:
            self._decodeVMEM(data)
        else:
            self._decodeVCED(data)
        
    def _decodeVCED(self,data):
        
        
        self.algorithm = data[8]
        self.feedback = data[9]
        self.oscSync = data[10]
        self.lfo = [data[i+11] for i in range(4)]
        self.lfoSync = data[15]
        self.lfoWave = data[16]
        self.pModSens = data[17]
        
    def _decodeVMEM(self,data):
        
        self.algorithm = data[110] & 0x1F
        self.oscSync = (data[111] >> 3) & 1
        self.feedback = data[111] & 7
        self.lfo = [data[i+112] for i in range(4)]
        self.pModSens = (data[116] >> 5) & 3 # TODO: resolove operation
        self.lfoWave = (data[116] >> 1) & 0xF
        self.lfoSync = data[116] & 1
              
        
class DX7voice:
    
    def __init__(self,data,bank=False):
        
        self.op = {}
        
        if bank:
            self._decodeVMEM(data)
        else:
            self._decodeVCED(data)
        
    def _decodeVCED(self,data):
        if len(data) != 155:
            raise Exception("Wrong voice size")
        pos = 0
        for i in range(6,0,-1):
            self.op[i] = DX7op(data[pos:pos+21])
            pos+=21 
               
        self.globals = DX7globals(data)
        self.name = data[145:155].tobytes().decode('utf-8')
      
    def _decodeVMEM(self,data):
        if len(data) != 128:
            raise Exception("Wrong voice size")
        pos = 0
        for i in range(6,0,-1):
            self.op[i] = DX7op(data[pos:pos+17],True)
            pos+=17 
               
        self.globals = DX7globals(data,True)
        self.name = data[118:128].tobytes().decode('utf-8') 
        
        

# Format Voice unique
class VCED:
    def __init__(self,data):
        self.voice = None
        self._analyse(data)
    
    def _analyse(self,data):
            
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
           
           
# Permet de décoder les Sysex de cartouches 32 voices de DX7 
class VMEM:
    def __init__(self,data):
        self.voices = None
        self._analyse(data)
    
    def _analyse(self,data):
            
        # En-tête + voice data
        if(len(data) != 4104):
            raise Exception("Size should be of 4104")
        
        sx = np.frombuffer(data,dtype=np.uint8)
        
        if(sx[0] != SX.start.value or sx[1] != SX.yamaha.value):
            raise Exception("Wrong sysex header")
        
        # l'octet 4 peux prendre deux valeurs: 0 pour une voice et 9 pour 32
        if(sx[3] != 9):
            raise Exception("Wrong sysex format: 32 voice bank expected")
        
        datasize = uint14(sx[4],sx[5])
        voiceSize = 128
        if (datasize!=4096):
            raise Exception("Wrong sysex data size")
        
        # On range la première voice en retirant l'en-tête 
        voices = [sx[6:voiceSize+6]]
        
        # On range dans la liste les 31 autres voices, avec 128 octets de décalage à chaque itération
        for i in range(31):
            offset = voiceSize*(i+1)
            voice = sx[offset:offset+voiceSize]
            voices.append(voice)
        
                
        # checksum = cheksum7(voice)
        # sxsk = sx[voiceSize+6]
        # if(sxsk != checksum):
        #     raise Exception("Wrong sysex checksum")
        
        if(sx[voiceSize*32+7] != SX.end.value):
            raise Exception("Wrong sysex end")
        
        self.voices = [DX7voice(voices[i],True) for i in range(32)]

def getVoice(path):
    with open(path,"rb") as file:
        data = file.read()
        vmem = VMEM(data)
        
        return vmem.voice
         

# https://forum.pdpatchrepo.info/uploads/files/1611522180187-sysex-format.txt