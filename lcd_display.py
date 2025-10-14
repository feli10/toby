from RPLCD.i2c import CharLCD
import time

# Use the address you saw in i2cdetect (often 0x27 or 0x3F)
lcd = CharLCD('PCF8574', 0x27)

try:
    while True:
        lcd.clear()
        lcd.write_string("Distance: 12.34cm")
        time.sleep(2)
        lcd.clear()
        lcd.write_string("Hello, world!")
        time.sleep(2)
except KeyboardInterrupt:
    lcd.clear()