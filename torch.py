import machine

spi_bus = machine.SPI.Bus(host=1, mosi=13, miso=12, sck=14)

touch_bus = machine.SPI.Bus(host=2, mosi=32, miso=39, sck=25)
touch_device = machine.SPI.Device(spi_bus=touch_bus, freq=2_000_000, cs=33)

import lcd_bus
display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=24_000_000, dc=2, cs=15)

import lvgl as lv
import ili9341
display = ili9341.ILI9341(
    data_bus=display_bus,
    display_width=320,
    display_height=240,
    backlight_pin=21,
    backlight_on_state=ili9341.STATE_PWM,
    color_space=lv.COLOR_FORMAT.RGB565,
    color_byte_order=ili9341.BYTE_ORDER_RGB,
    rgb565_byte_swap=1
)
display.set_power(True)
display.init(1)

display._ORIENTATION_TABLE = (0xE0, 0x0, 0x0, 0x0)
display.set_rotation(lv.DISPLAY_ROTATION._0)
display.set_backlight(100)

import xpt2046

class _TouchCal:
    # Identity affine transform + X&Y-axis mirror to correct hardware orientation.
    alphaX = 0.0; betaX = 1.33333; deltaX = 0.0
    alphaY = 0.75; betaY = 0.0; deltaY = 0.0
    mirrorX = True
    mirrorY = True

indev = xpt2046.XPT2046(device=touch_device, touch_cal=_TouchCal())

import task_handler
task_handler.TaskHandler()

from machine import PWM, Pin

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

scr = lv.screen_active()

COLORS = [
    ("Red",   0xFF0000),
    ("Green", 0x00FF00),
    ("Blue",  0x0000FF),
    ("White", 0xFFFFFF),
]

BTN_W = 100
BTN_H = 60
GAP = 10
START_X = (320 - BTN_W * 2 - GAP) // 2
START_Y = (240 - BTN_H * 2 - GAP) // 2

_current_color = None

def make_color_cb(color_hex):
    def cb(evt):
        global _current_color
        if _current_color == color_hex:
            _current_color = None
            scr.set_style_bg_color(lv.color_hex(0x000000), 0)
            scr.set_style_bg_opa(lv.OPA.COVER, 0)
            set_led(0x000000)
        else:
            _current_color = color_hex
            scr.set_style_bg_color(lv.color_hex(color_hex), 0)
            scr.set_style_bg_opa(lv.OPA.COVER, 0)
            set_led(color_hex)
    return cb

for i, (name, color_hex) in enumerate(COLORS):
    col = i % 2
    row = i // 2

    btn = lv.button(scr)
    btn.set_size(BTN_W, BTN_H)
    btn.set_pos(START_X + col * (BTN_W + GAP), START_Y + row * (BTN_H + GAP))

    style = lv.style_t()
    style.init()
    style.set_bg_color(lv.color_hex(color_hex))
    style.set_bg_opa(lv.OPA.COVER)
    if color_hex == 0xFFFFFF:
        style.set_text_color(lv.color_hex(0x000000))
    btn.add_style(style, 0)

    label = lv.label(btn)
    label.set_text(name)
    label.center()

    btn.add_event_cb(make_color_cb(color_hex), lv.EVENT.CLICKED, None)
