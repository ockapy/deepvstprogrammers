from Create_sysex import sysex_from_patch
from sysexConverter import Converter
import sysex_data_extractor as sd

bank = sd.getVoice('app/VST/SynprezFM_01.syx')
patches = sd.bankToPatches(bank)

sysex_from_patch(patches[0])

print("ok")