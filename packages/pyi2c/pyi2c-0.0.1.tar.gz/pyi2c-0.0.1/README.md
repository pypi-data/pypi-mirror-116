# A useful i2c Python3 package for Pi
Based on smbus2


## Installation
Via pip
```
pip3 install pyi2c
```

## How to use?
Example
```
from pyi2c import I2C

# Create i2c
BUS_N = 0 # 0 or 1 or 2. Change this to yours
i2c = I2C(BUS_N)

# Write
ADDR = 0x38 # Change this to yours
WRITE1 = 0x00 # Change this to yours
i2c.write(ADDR, WRITE)
# or write multi bytes, up to 64 bytes
WRITE0 = 0x01 # Change this to yours
i2c.write(ADDR, [WRITE0, WRITE1])

# Read
read_data = i2c.read(ADDR)
# or set length of reading bytes
bytes_n = 2
read_data = i2c.read(ADDR, byte_n)

# First write and read rapidly
read_data = i2c.writeread(ADDR, WRITE0)
# These also work
read_data = i2c.writeread(ADDR, [WRITE0, WRITE1])
read_data = i2c.writeread(ADDR, [WRITE0, WRITE1], bytes_n)
```



## Reference
- [smbus2 GitHub](https://github.com/kplindegaard/smbus2)
- [Pure Python I2C : access to I2C components through serial or parallel interface.](http://pyi2c.sourceforge.net/)
