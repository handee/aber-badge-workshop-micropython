from machine import PWM, Pin
import urandom
import time

# Active-low RGB LED: duty_u16=0 - full on, 65535 - off
_led_r = PWM(Pin(4), freq=1000, duty_u16=65535)
_led_g = PWM(Pin(16), freq=1000, duty_u16=65535)
_led_b = PWM(Pin(17), freq=1000, duty_u16=65535)

def set_led(color_hex):
    r = (color_hex >> 16) & 0xFF
    g = (color_hex >> 8) & 0xFF
    b = color_hex & 0xFF
    _led_r.duty_u16(65535 - r * 257)
    _led_g.duty_u16(65535 - g * 257)
    _led_b.duty_u16(65535 - b * 257)

def random_color():
    bits = urandom.getrandbits(3)
    r = 0xFF if bits & 0b100 else 0x00
    g = 0xFF if bits & 0b010 else 0x00
    b = 0xFF if bits & 0b001 else 0x00
    return (r << 16) | (g << 8) | b

def fade(start, end, steps=50, delay_ms=20):
    sr = (start >> 16) & 0xFF
    sg = (start >> 8) & 0xFF
    sb = start & 0xFF
    er = (end >> 16) & 0xFF
    eg = (end >> 8) & 0xFF
    eb = end & 0xFF
    for i in range(steps + 1):
        t = i / steps
        r = int(sr + (er - sr) * t)
        g = int(sg + (eg - sg) * t)
        b = int(sb + (eb - sb) * t)
        set_led((r << 16) | (g << 8) | b)
        time.sleep_ms(delay_ms)


start = 0x0

while True:
    end = random_color()
    fade(start, end)
    start = end

