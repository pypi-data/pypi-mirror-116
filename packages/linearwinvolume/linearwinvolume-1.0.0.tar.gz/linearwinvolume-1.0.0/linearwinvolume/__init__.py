'''linearWinVolume is a package that controls the default sound device's
volume in Windows in a percentage form as opposed to PyCaw's logarithmic
scale. After a configuration through linearwinvolume.setup(), win_volume
accurately converts the dB input to an easily readable 0-100 scale'''

import numpy
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import os
import configparser
import sounddevice as sd

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
    samples = int(input('Enter maximum number of samples to input: '))
    vol_db = [min_vol*(x/samples)+max_vol for x in range(samples)]
    vol_percent = []
    for value in vol_db:
        volume.SetMasterVolumeLevel(value, None)
        vol_level = float(input('Input Current Volume: '))
        if vol_level != 0:
            vol_percent.append(vol_level)
        else:
            break
    vol_db = vol_db[:len(vol_percent)]
    log_fit = numpy.polyfit(numpy.log(vol_percent),vol_db,1)

    config[sd.query_devices(None,'output')['name']] = {
        'Natural logarithm coeff':str(log_fit[0]),
        'Constant offset':str(log_fit[1]),
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

vol_percent = [100.0, 78.0, 60.0, 47.0, 36.0, 28.0, 22.0, 17.0, 13.0, 10.0, 8.0, 6.0, 5.0, 4.0, 3.0, 2.0, 2.0, 1.0, 1.0, 1.0]

@config_check
def set_volume(value):
    '''Sets the Windows host's volume to a certain percent from the derived logarithmic
    values in the volume.conf'''
    constant = float(config[sd.query_devices(None,'output')['name']]['constant offset'])
    coeff = float(config[sd.query_devices(None,'output')['name']]['natural logarithm coeff'])
    min_vol = float(config[sd.query_devices(None,'output')['name']]['min_vol'])
    max_vol = float(config[sd.query_devices(None,'output')['name']]['max_vol'])
    if value >= 100:
        volume.SetMasterVolumeLevel(max_vol, None)
    elif value <= 0:
        volume.SetMasterVolumeLevel(min_vol, None)
    else:
        vol = constant + coeff * numpy.log(value)
        volume.SetMasterVolumeLevel(vol, None)

@config_check
def get_volume():
    '''Retrieves the Windows host's volume and returns a percent'''
    constant = float(config[sd.query_devices(None,'output')['name']]['constant offset'])
    coeff = float(config[sd.query_devices(None,'output')['name']]['natural logarithm coeff'])
    db = volume.GetMasterVolumeLevel()
    return int(numpy.exp((db-constant)/coeff))

def change_volume(value):
    '''Changes volume by the input value, can both raise and lower value, if the value goes
    above 100, or below 0, set_volume catches the error and just sets it to 100 and 0 percent
    respectively'''
    set_volume(get_volume() + value)