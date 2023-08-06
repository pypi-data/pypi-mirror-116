'''linearWinVolume is a package that controls the default sound device's
volume in Windows in a percentage form as opposed to PyCaw's logarithmic
scale. After a configuration through linearwinvolume.setup(), linearWinVolume
accurately converts the dB input to an easily readable 0-100 scale'''

import numpy
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from numpy.lib.function_base import _corrcoef_dispatcher
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import os
import configparser
import sounddevice as sd
from scipy.special import lambertw

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
workingDir = os.path.dirname(os.path.realpath(__file__))+os.path.sep
config = configparser.ConfigParser()
config.read(workingDir+'volume.conf')

def setup():
    '''Creates/Updates volume.conf and its values within an interactive python terminal'''
    print('#'*41+'\nWindows Volume Setup Command Line Utility\n'+'#'*41+'\n')

    if os.path.isfile(workingDir+"volume.conf"):
        print('[INFO] Found existing configuration, will be updated\n')
    
    min_vol, max_vol, null = volume.GetVolumeRange()
    print("This utility takes a number of samples of your computer's volume levels")
    print("and uses it in conjunction with the dB values for your sound device in ")
    print("order to create a logarithmic relationship between Windows' displayed ")
    print("volume number and the dB value from pycaw.\n")

    input("This program relies on your input of Windows' volume values; press Enter to open Settings now")
    os.system("start \"\" ms-settings:sound")
    samples = int(input('Enter maximum number of samples to input (Recommended: 15+): '))
    print('') # New line Spacer
    vol_db = [min_vol*(x/samples)+max_vol for x in range(samples)]
    vol_percent = []
    for value in vol_db:
        volume.SetMasterVolumeLevel(value, None)
        print('Set volume to ',value, 'dB')
        vol_level = float(input('Input Current Volume: '))
        if vol_level != 0:
            vol_percent.append(vol_level)
        else:
            break
    vol_db = vol_db[:len(vol_percent)]
    coeff, constant = numpy.polyfit(numpy.log(vol_percent),vol_db,1)
    correction_coeff = 0

    print("\nA logarithmic fit is occasionally not a perfect fit for Windows'")
    print("volume scaling.\n")
    ans = input("Would you like to preform a linear correction? (y/n): ").lower()

    if ans == 'y':
        print("\nEnter any letter if volume displayed MATCHES Windows' Volume")
        print("otherwise press the Enter key to go to the next value\n")
        
        config[sd.query_devices(None,'output')['name']] = {
        'Natural logarithm coeff':str(coeff),
        'Constant offset':str(constant),
        'Correction coeff':str(correction_coeff),
        'min_vol':str(min_vol),
        'max_vol':str(max_vol),
        'samples':str(samples)
        }

        for i in list(range(100))[::-1]:
            set_volume(i)
            ans = input('Guessed Volume Level: {} '.format(i))
            if ans != '':
                intersect = i
                break

        run = 100-intersect
        rise = max_vol - (constant + coeff * numpy.log(100))
        correction_coeff = rise/run
        constant_2 = max_vol - (constant + coeff * numpy.log(100) + correction_coeff * 100)
        constant = constant + constant_2

    config[sd.query_devices(None,'output')['name']] = {
        'Natural logarithm coeff':str(coeff),
        'Constant offset':str(constant),
        'Correction coeff':str(correction_coeff),
        'min_vol':str(min_vol),
        'max_vol':str(max_vol),
        'samples':str(samples)
    }
    
    with open(workingDir+'volume.conf','w') as configfile:
        config.write(configfile)
    
    print('Wrote changes to config file at: '+workingDir+'volume.conf')

def config_check(func):
    '''Checks if a configuration for the current sound device exists, otherwise prints an error message.
    However, does not stop execution.'''
    def inner(*args, **kwargs):
        try:
            config[sd.query_devices(None,'output')['name']]
            return func(*args, **kwargs)
        except KeyError as e:
            print('Configuration for {} does not exist, please run win_volume.setup() to create config'.format(sd.query_devices(None,'output')['name']))
            print(e)
    return inner

@config_check
def set_volume(value):
    '''Sets the Windows host's volume to a certain percent from the derived logarithmic
    values in the volume.conf'''
    constant = float(config[sd.query_devices(None,'output')['name']]['constant offset'])
    coeff = float(config[sd.query_devices(None,'output')['name']]['natural logarithm coeff'])
    correction_coeff = float(config[sd.query_devices(None,'output')['name']]['correction coeff'])
    min_vol = float(config[sd.query_devices(None,'output')['name']]['min_vol'])
    max_vol = float(config[sd.query_devices(None,'output')['name']]['max_vol'])
    if value >= 100:
        volume.SetMasterVolumeLevel(max_vol, None)
    elif value <= 0:
        volume.SetMasterVolumeLevel(min_vol, None)
    else:
        vol = constant + coeff * numpy.log(value) + correction_coeff * value
        if vol >= max_vol:
            volume.SetMasterVolumeLevel(max_vol, None)
        elif vol <= min_vol:
            volume.SetMasterVolumeLevel(min_vol, None)
        else:
            volume.SetMasterVolumeLevel(vol, None)

@config_check
def get_volume():
    '''Retrieves the Windows host's volume and returns a percent'''
    constant = float(config[sd.query_devices(None,'output')['name']]['constant offset'])
    coeff = float(config[sd.query_devices(None,'output')['name']]['natural logarithm coeff'])
    correction_coeff = float(config[sd.query_devices(None,'output')['name']]['correction coeff'])
    db = volume.GetMasterVolumeLevel()

    # return int(numpy.exp((db-constant)/coeff)) # valid for correction_coeff = 0

    lambert_eval = (correction_coeff * numpy.exp((db/coeff) - (constant/coeff)))
    return int(round(numpy.real((coeff * lambertw(lambert_eval/coeff))/correction_coeff)))

def change_volume(value):
    '''Changes volume by the input value, can both raise and lower value, if the value goes
    above 100, or below 0, set_volume catches the error and just sets it to 100 and 0 percent
    respectively'''
    set_volume(get_volume() + value)