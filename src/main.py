from machine import Pin, ADC, I2C
i2c = I2C(1, freq=100000, scl=Pin(25), sda=Pin(26))
adc = ADC(Pin(32))
adc.atten(ADC.ATTN_11DB)  # 3.6V
adc.width(ADC.WIDTH_9BIT) # 0..511
I2C_ADDR = 0x2C
inst_byte = 0b00000_000
def printI2CDevices():
    print('Scan i2c bus...')
    devices = i2c.scan()
    print('Found {0} I2C device(s): '.format(len(devices)), end='')
    for device in devices:  
        print('{0} '. format(hex(device)), end='')
    print()
def loop():
    while True:
        data_byte = int(input("Enter position (0..255): "))
        if data_byte == -1:
            printI2CDevices()
        elif data_byte == -2:
            buf = i2c.readfrom(I2C_ADDR, 1)
            print('Position:', buf[0])
        else:
            i2c.writeto(I2C_ADDR, bytes([inst_byte, data_byte]))
            print('ADC value: ', int(adc.read() / 2))
try:
    loop()
except KeyboardInterrupt:
    print('Got Ctrl-C')
finally:
    print("Finishing...")
