# 2025 Fall ECE Senior Design Miniproject

[Project definition](./Project.md)

This project uses the Raspberry Pi Pico 2WH SC1634 (wireless, with header pins).

Each team must provide a micro-USB cable that connects to their laptop to plug into the Pi Pico.
The cord must have the data pins connected.
Splitter cords with multiple types of connectors fanning out may not have data pins connected.
Such micro-USB cords can be found locally at Microcenter, convenience stores, etc.
The student laptop is used to program the Pi Pico.
The laptop software to program and debug the Pi Pico works on macOS, Windows, and Linux.

This miniproject focuses on using
[MicroPython](./doc/micropython.md)
using
[Thonny IDE](./doc/thonny.md).
Other IDE can be used, including Visual Studio Code or
[rshell](./doc/rshell.md).

## Project Setup

### Software/Circuitry
1. Connect the Pico 2W to the Raspberry Pi Pico breakout board 
2. After launching Thonny IDE, hold the BOOTSEL button on your Raspberry Pi while plugging the micro-USB cable.
3. Install the MicroPython Firmware on the Pico, check to make sure the interpreter is set to Pico 2W specifically. 
 
#### Photoresistor (Light Sensor)
Given a photoresistor and a 10k ohm resistor, wiring the photoresistor to GND and GP28 and the resistor to GP28 and 3V3 power source forms a voltage divider. 

The voltage divider dictates the output voltage, which depends on the ratio of the two resistors. As light increases, the resistance of the photoresistor decreases, changing the voltage at GP28. The ADC (analog to digital converter) then measures that voltage and determines the light level based on the observed value. j

The ADC reading is a 16-bit value from 0-65535, proportional to light intensity. 

```
photo_sensor_pin = ADC(28)

light_value = photo_sensor_pin.read_u16()

frequency = map_value(clamped_light, min_light, max_light,
                              min_freq, max_freq)  
```

#### Piezo Buzzer (Sound Output) 
PWM (Pulse Width Modulation) can be used to generate square waves at specific frequencies, which correspond to different musical notes at various duty cycles. 

```
from machine import Pin, PWM
import time

buzzer_pin = PWM(Pin(16))

volume = map_value(clamped_light, min_light, max_light,
                              min_vol, max_vol)
```

The map_value function as mentioned above, returns the frequency or duty cycle outputs based on light input. While stop_tone turns the duty cycle to 0. 

```
def stop_tone():
    buzzer_pin.duty_u16(0)

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
```

#### Two Modes: Volume and Frequency
The hardware can operate in two different modes, controlled by the mode argument passed to main(). 

1. Volume main(mode="volume")
- The level of light controls the volume. A brighter light level lowers the volume.
- The pitch is modulated to the tune of "Twinkle Twinkle Little Star."
- See an example of volume mode [here](https://drive.google.com/file/d/1fm6gHLpvCDpJNjy5oRp4q0sUcNiw9mwe/view?usp=sharing)

```
def volume_control(min_light, max_light, light_value):
    min_vol = 1000
    max_vol = 32768
    clamped = max(min_light, min(light_value, max_light))

    if clamped > min_light:
        global volume
        volume = map_value(clamped, min_light, max_light, min_vol, max_vol)
    else:
        buzzer_pin.duty_u16(0)        # Silence
```

2. Frequency Mode main(mode="freq")
- Light level controls pitch.
- Volume is fixed at 50%.
- Pitch ranges from C4 to C6.
- See an example of frequency mode [here](https://drive.google.com/file/d/1pfGwG24YXPZGF0LfyjeGqt3t_GSveV5C/view?usp=sharing)

```
def freq_control(min_light, max_light, light_value):
    min_freq = 261    # C4
    max_freq = 1046   # C6
    clamped = max(min_light, min(light_value, max_light))

    if clamped > min_light:
        frequency = map_value(clamped, min_light, max_light, min_freq, max_freq)
        buzzer_pin.freq(frequency)
        buzzer_pin.duty_u16(32768)    # Fixed loudness
    else:
        buzzer_pin.duty_u16(0)
```

## Hardware

* Raspberry Pi Pico WH [SC1634](https://pip.raspberrypi.com/categories/1088-raspberry-pi-pico-2-w) (WiFi, Bluetooth, with header pins)
* Freenove Pico breakout board [FNK0081](https://store.freenove.com/products/fnk0081)
* Piezo Buzzer SameSky CPT-3095C-300
* 10k ohm resistor
* 2 [tactile switches](hhttps://www.mouser.com/ProductDetail/E-Switch/TL59NF160Q?qs=QtyuwXswaQgJqDRR55vEFA%3D%3D)

### Photoresistor details

The photoresistor uses the 10k ohm resistor as a voltage divider
[circuit](./doc/photoresistor.md).
The 10k ohm resistor connects to "3V3" and to ADC2.
The photoresistor connects to the ADC2 and to AGND.
Polarity is not important for this resistor and photoresistor.

The MicroPython
[machine.ADC](https://docs.micropython.org/en/latest/library/machine.ADC.html)
class is used to read the analog voltage from the photoresistor.
The `machine.ADC(id)` value corresponds to the "GP" pin number.
On the Pico W, GP28 is ADC2, accessed with `machine.ADC(28)`.

### Piezo buzzer details

PWM (Pulse Width Modulation) can be used to generate analog signals from digital outputs.
The Raspberry Pi Pico has eight PWM groups each with two PWM channels.
The [Pico WH pinout diagram](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf)
shows that almost all Pico pins can be used for multiple distinct tasks as configured by MicroPython code or other software.
In this exercise, we will generate a PWM signal to drive a speaker.

GP16 is one of the pins that can be used to generate PWM signals.
Connect the speaker with the black wire (negative) to GND and the red wire (positive) to GP16.

In a more complete project, we would use additional resistors and capacitors with an amplifer to boost the sound output to a louder level with a bigger speaker.
The sound output is quiet but usable for this exercise.

Musical notes correspond to particular base frequencies and typically have rich harmonics in typical musical instruments.
An example soundboard showing note frequencies is [clickable](https://muted.io/note-frequencies/).
Over human history, the corresspondance of notes to frequencies has changed over time and location and musical cultures.
For the question below, feel free to use musical scale of your choice!

[Music Examples](https://github.com/twisst/Music-for-Raspberry-Pi-Pico/blob/main/play.py)


## Notes

Pico MicroPython time.sleep() doesn't error for negative values even though such are obviously incorrect--it is undefined for a system to sleep for negative time.
Duty cycle greater than 1 is undefined, so we clip the duty cycle to the range [0, 1].


## Reference

* [Pico 2WH pinout diagram](https://datasheets.raspberrypi.com/picow/pico-2-w-pinout.pdf) shows the connections to analog and digital IO.
* Getting Started with Pi Pico [book](https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf)
