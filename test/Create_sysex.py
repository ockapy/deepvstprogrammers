
def transform_to_voice(patch):

    voice_params = patch[0:23]
    operators = patch[23:155]
    
    data = bytearray()
    
    encoded_header = encode_header()
    
    voices = bytearray()
    for i in range(32):
        encoded_operators = encode_Operators(operators)
        encoded_voice = encode_voice(voice_params)
        
        voices.extend(encoded_operators)
        voices.extend(encoded_voice)
    
    print("Encoded operators:", encoded_operators)
    
    checksum = compute_checksum(voices)
    
    data.extend(encoded_header)
    data.extend(voices)
    data.append(checksum)
    data.append(0xF7)
    
    print(len(data))
    return data    
    
def encode_header():
    data = bytearray()
    data.append(0xF0) # Status Byte - start sysex
    data.append(0x43) # ID (67 = Yamaha)
    data.append(0x00) # Sub-status & Channel number
    data.append(0x09) # Format number (9 = 32 voices)
    data.append(0x20) # Byte count MS byte
    data.append(0x00) # Byte count LS byte  
    
    return data
    

def encode_Operators(operators):
    data = bytearray()
    offset = 22  
    
    opList = []

    for i in range(6):
        start_index = i * offset
        end_index = (i + 1) * offset
        encoded_operator = encode_Operator(operators[start_index:end_index])
        opList.insert(0,encoded_operator)
    
    for operator in opList:
        data.extend(operator)
        
    return data

def encode_Operator(operator):
    # Ensure each value fits into its respective bit range
    pitch_rate = [round(value * 99) for value in operator[0:4]]
    pitch_level = [round(value * 99) for value in operator[4:8]]
    output_level = round(operator[8] * 99) # Mauvais parsing
    osc_mode = round(operator[9])
    freq_coarse = round(operator[10] * 31) # Mauvais parsing
    freq_fine = round(operator[11] * 99) # Mauvais parsing
    detune = round(operator[12] * 14) # Mauvais parsing
    break_point = round(operator[13] * 99)
    l_scale_depth = round(operator[14] * 99)
    r_scale_depth = round(operator[15] * 99) # Mauvais parsing
    l_key_curve = round(operator[16]*3)
    r_key_curve = round(operator[17]*3) # Mauvais parsing
    osc_rate_scale = round(operator[18] * 7) # Mauvais parsing
    amp_mod_sens = round(operator[19] * 3)
    key_vel_sens = round(operator[20] * 7) # Mauvais parsing
    
    if (break_point > 99 or break_point < 0):
        raise Exception("break_point not in range 0-99")
    if (l_scale_depth > 99 or l_scale_depth < 0):
        raise Exception("Left Scale depth not in range 0-99")
    if (r_scale_depth > 99 or r_scale_depth < 0):
        raise Exception("Right Scale depth not in range 0-99")
    if (l_key_curve > 3 or l_key_curve < 0):
        raise Exception("Left key curve not in range 0-3")
    if (r_key_curve > 3 or r_key_curve < 0):
        raise Exception("Right key curve value not in range 0-3")
    if (detune > 14 or detune < 0):
        raise Exception("Detune not in range 0-17")
    if (osc_rate_scale > 7 or osc_rate_scale < 0):
        raise Exception ("Oscillator rate scale not in range 0-7")
    if (key_vel_sens > 7 or key_vel_sens < 0):
        raise Exception("Key velocity sensibility not in range 0-7")
    if (amp_mod_sens > 3 or amp_mod_sens < 0 ):
        raise Exception("AMP modulation sensibility not in range 0-3")
    if (output_level > 99 or output_level < 0):
        raise Exception("Output level not in range 0-99")
    if (freq_coarse > 31 or freq_coarse < 0):
        raise Exception("Frequency coarse not in range 0-31")
    if (osc_mode != 0 and osc_mode !=1):
        raise Exception("Osicllator mode not 0 or 1")
    if (freq_fine > 99 or freq_fine < 0):
        raise Exception("Frequency fine not in range 0-99")
    
    
    # Create a bytearray to store the encoded data
    data = bytearray()

    # Byte 0-7: OP6 EG R1-R4, OP6 EG L1-L4
    for value in pitch_rate:
        if (value > 99 or value <0):
            raise Exception("Pitch rate value not in range 0-99")
        else:
            data.append((value))

    for value in pitch_level:
        if (value > 99 or value < 0):
            raise Exception("Pitch level value not in range 0-99")
        else:
            data.append((value))

    # Byte 8: LEV SCL BRK PT
    data.append((break_point))

    # Byte 9-10: SCL LEFT DEPTH, SCL RIGHT DEPTH
    data.extend(([l_scale_depth, r_scale_depth]))

    # Byte 11: SCL LEFT CURVE (bits 2-0), SCL RIGHT CURVE (bits 5-3)
    curve_byte = (l_key_curve & 0b11) | ((r_key_curve & 0b11) << 2)
    data.append(curve_byte)

    # Byte 12: OSC DETUNE (bits 4-0), OSC RATE SCALE (bits 6-4)
    detune_rate_byte = ((osc_rate_scale & 0b111) | ((detune & 0b1111) << 3))
    data.append(detune_rate_byte)

    # Byte 13: KEY VEL SENS (bits 2-0), AMP MOD SENS (bits 5-4)
    vel_mod_byte = ((amp_mod_sens & 0b11) | ((key_vel_sens & 0b111) << 2))
    data.append(vel_mod_byte)

    # Byte 14: OP6 OUTPUT LEVEL
    data.append(output_level)

    # Byte 15: FREQ COARSE (bits 4-0), OSC MODE (bit 7)
    coarse_mode_byte = ((osc_mode & 0b1)) | ((freq_coarse & 0b11111) << 1)
    
    data.append(coarse_mode_byte)

    # Byte 16: FREQ FINE
    data.append(freq_fine)

    # Verify the length of the data (number of bytes)
    print(len(data))

    return bytes(data)
    
def encode_voice(voice):
    data = bytearray()
    
    pitch_eg_rate = [round(value*99) for value in voice[15:19]]
    pitch_eg_level = [round(value*99) for value in voice[19:23]]
    
    algorithm = round(voice[4]*31)
    osc_key_sync = round(voice[6])
    feedback = round(voice[5]*7)
    lfo_speed = round(voice[7]*99)
    lfo_delay = round(voice[8]*99)
    lfo_pm_depth = round(voice[9]*99)
    lfo_am_depth = round(voice[10]*99)
    lfo_pm_sens = round(voice[14]*7)
    lfo_wave = round(voice[12]*5)
    lfo_key_sync = round(voice[11])
    
    if (algorithm > 31 or algorithm < 0): raise Exception("Algorithm not in range 0-31")
    if (osc_key_sync > 1 or osc_key_sync < 0): raise Exception("Oscillator key sync not in range 0-1")
    if (feedback > 7 or feedback < 0): raise Exception("Feedback not in range 0-7")
    if (lfo_speed > 99 or lfo_speed < 0): raise Exception("LFO Speed not in range 0-99")
    if (lfo_delay > 99 or lfo_delay < 0): raise Exception("LFO Delay not in range 0-99")
    if (lfo_pm_depth > 99 or lfo_pm_depth < 0): raise Exception("LFO PM Depth not in range 0-99")
    if (lfo_am_depth > 99 or lfo_am_depth < 0): raise Exception("LFO AM Depth not in range 0-99")
    if (lfo_pm_sens > 7 or lfo_pm_sens < 0): raise Exception("LFO PM Sens not in range 0-7")
    if (lfo_wave > 5 or lfo_wave < 0): raise Exception("LFO Wave not in range 0-5")
    if (lfo_key_sync > 1 or lfo_key_sync < 0): raise Exception("LFO Key Sync not in range 0-1")
    
    for value in pitch_eg_rate:
        if (value > 99 or value < 0):
            raise Exception("Pitch eg rate value not in range 0-99")
        else:
            data.append(value)
    
    for value in pitch_eg_level:
        if (value > 99 or value < 0):
            raise Exception("Pitch eg rate value not in range 0-99")
        else:
            data.append(value)
    
    data.append(algorithm)
    
    osc_key_sync_feedback_byte = ((feedback & 0b111)|((osc_key_sync & 0b1) << 3))
    data.append(osc_key_sync_feedback_byte)
    
    data.append(lfo_speed)
    data.append(lfo_delay)
    data.append(lfo_pm_depth)
    data.append(lfo_am_depth)
    
    lpms_lfw_lks_byte =  ((lfo_key_sync & 0b1) | ((lfo_wave & 0b111) << 1) | ((lfo_pm_sens & 0b111) << 4))
    data.append(lpms_lfw_lks_byte)
    
    data.append(24) # transpose
    
    data.append(0x74)
    data.append(0x65)
    data.append(0x73)
    data.append(0x74)
    data.append(0x0A)
    data.append(0x0A)       # ASCII for test 
    data.append(0x00)
    data.append(0x00)
    data.append(0x00)
    data.append(0x00)
    
    return data


def compute_checksum(data):
    # Ensure data is exactly 4096 bytes
    if len(data) != 4096:
        raise ValueError("Data must be exactly 4096 bytes")
    
    # Calculate the sum of all bytes
    total_sum = sum(data)
    
    # Apply a mask to ensure the sum fits within an 8-bit range
    masked_sum = total_sum & 0xFF
    
    # Compute the 2's complement
    checksum = (~masked_sum + 1) & 0xFF
    
    return checksum



def sysex_from_patch(patch):
    data=transform_to_voice(patch)
    
    with open("patch.syx",'wb') as file:
        file.write(data)
    print ("sysex created")