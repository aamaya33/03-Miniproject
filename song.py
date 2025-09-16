import machine
import time

# --- Pin Configuration ---
photo_sensor_pin = machine.ADC(28)
buzzer_pin = machine.PWM(machine.Pin(16))

# --- Music Definition ---
# Notes mapped to frequencies (in Hz)
C4 = 262
D4 = 294
E4 = 330
F4 = 349
G4 = 392
A4 = 440
B4 = 494
C5 = 523

# A simple melody: "Twinkle, Twinkle, Little Star"
# Format: (note_frequency, duration_in_ms)
SONG = [
    (C4, 400),
    (C4, 400),
    (G4, 400),
    (G4, 400),
    (A4, 400),
    (A4, 400),
    (G4, 800),
    (F4, 400),
    (F4, 400),
    (E4, 400),
    (E4, 400),
    (D4, 400),
    (D4, 400),
    (C4, 800),
]

def stop_tone():
    buzzer_pin.duty_u16(0)

def play_song():
    for frequency, duration in SONG:
        buzzer_pin.freq(frequency)
        buzzer_pin.duty_u16(32768)  # 50% duty cycle
        time.sleep_ms(int(duration * 0.9)) # more akin to music, the rest is proportional to the note duration
        stop_tone()
        time.sleep_ms(int(duration * 0.1))
        
        
        

def main():
    try:
    
        while True:
           play_song()

    except KeyboardInterrupt:
        stop_tone()
        print("Stopped.")

# Run main loop
main()

