import time

print("Starting...")

import machine
spi_bus = machine.SPI.Bus(host=1, mosi=13, sck=14)

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
     color_byte_order=ili9341.BYTE_ORDER_BGR,
     rgb565_byte_swap=1
)
display.set_power(True)
display.init(1)

display._ORIENTATION_TABLE = (0xE0, 0x0, 0x0, 0x0)
display.set_rotation(lv.DISPLAY_ROTATION._0)

display.set_backlight(100)
import task_handler
task_handler.TaskHandler()

scr = lv.screen_active()
label = lv.label(scr)
label.set_text("Hello world!")
label.center()