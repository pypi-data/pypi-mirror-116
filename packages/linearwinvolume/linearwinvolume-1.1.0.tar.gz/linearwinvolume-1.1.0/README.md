# linearWinVolume
 > A Python implementation of pycaw that doesn't function on a decibel scale

In order to linearly interface with Windows' volume control in a manner that matches the UI's output, linearWinVolume computes a logarithmic regression from user collected sample data points. From there it optionally applies a linear correction value such that when setting and getting the volume state it is accurate to rougly ~1 unit of Windows volume at all times.

## Installation

Windows:

```bash
pip install linearwinvolume
```
Setup (Need to setup every sound device individually):
```python
# With desired sound device as Output Device under windows
import linearwinvolume
linearwinvolume.setup()
# From here, follow the CLI prompts to callibrate your sound device's dB levels
```
In order to complete setup:
1) Select a sample size of data points (Windows volume units)
2) Input Windows volume values until Windows volume is 0
3) (OPTIONAL) Compute a linear correction
    * This massively improves accuracy on some sound devices
    * The setup function will count down from 100 to 0 setting your volume accordingly
    * Enter any letter once the guessed value matches the true Windows value

## Usage examples

This python module offers 4 functions. The first, ```linearwinvolume.setup()```, is used to callibrate the sound device. The rest are:
```python
# Set volume to 55%
linearwinvolume.set_volume(55)

# Get current volume, returns integer from 0 - 100
linearwinvolume.get_volume()

# Change volume, to increase volume, use a positive integer, to decrease use a negative value
linearwinvolume.change_volume()
```

## Explanation

In order to derive an equation that accurately represents all volume values form 0 to 100, a logarithmic regression is preformed on the collected sample values.

Initially, the program computes the logarithmic regression which takes the form of ```y = A ln(x) + B```

Oftentimes, this is enough to maintain ~1 unit of Windows volume unit error.

In order to improve accuracy on some devices, an additional linear term is added such that the new function takes the form of ```y = A ln(x) + C x + (B + D)```

C is defined as 100 - intersect divided by the max volume in Db - initial logarithmic regression for x =100

D is defined as the difference between the max volume and ```y = A ln(x) + C x + B``` solved for x = 100

Using Mathematica, the resultant equation, ```y = A ln(x) + C x + (B + D)```, is solved for x, to reveal a new [Equation](https://www.wolframalpha.com/input/?i=%28A+ProductLog%28%28C+e%5E%28-B%2FA+%2B+y%2FA%29%29%2FA%29%29%2FC), in order to use the get_volume() function. As a result of it using the Lambert W function W(z), this package requires scipy.

The configuration file where values are saved is stored inside the pip directory and is global for a python installation. It takes the form of:

```ini
[Headset (Headphone adapter)]
natural logarithm coeff = 10.690485218963337
constant offset = -54.99262202770247
correction coeff = 0.05761118223586133
min_vol = -50.0
max_vol = 0.0
samples = 25
```

## Release History

* 1.1.0
    * Added linear correction algorithm that dramatically improves accuracy on some devices
* 1.0.0
    * Initial Release

## Credits

Adrian Ornelas – afornelas@outlook.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/That-CC](https://github.com/That-CC)


