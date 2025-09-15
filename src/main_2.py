# main_offline.py
import machine
import time

# --- Pin Configuration ---
photo_sensor_pin = machine.ADC(28)
buzzer_pin = machine.PWM(machine.Pin(16))

def stop_tone():
    buzzer_pin.duty_u16(0)

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def main():
    try:
        while True:
            # Read the sensor (0–65535)
            light_value = photo_sensor_pin.read_u16()
            # Clamp and map
            min_light = 1000
            max_light = 65000
            min_freq = 261   # C4
            max_freq = 1046  # C6
            clamped_light = max(min_light, min(light_value, max_light))

            if clamped_light > min_light:
                frequency = map_value(clamped_light, min_light, max_light,
                                      min_freq, max_freq)
                buzzer_pin.freq(frequency)
                buzzer_pin.duty_u16(32768)  # 50% duty cycle
            else:
                stop_tone()

            time.sleep_ms(50)

    except KeyboardInterrupt:
        stop_tone()
        print("Stopped.")

# Run main loop
main()
