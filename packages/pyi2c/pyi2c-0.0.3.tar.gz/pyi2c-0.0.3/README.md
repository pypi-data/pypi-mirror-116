# A useful i2c Python3 package for Pi
It is a simple I2C interface based on smbus2.



## 1. Installation
Via [pip](https://pypi.org/project/pyi2c/)
```
pip3 install pyi2c
```



## 2. How to use I2C? (Example)
### 2.1 Write
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
```

### 2.2 Read
```
from pyi2c import I2C

# Create i2c
BUS_N = 0 # 0 or 1 or 2. Change this to yours
i2c = I2C(BUS_N)

# Read
read_data = i2c.read(ADDR)

# or set length of reading bytes
bytes_n = 2
read_data = i2c.read(ADDR, byte_n)

```

### 2.3 Write and read
```
from pyi2c import I2C

# Create i2c
BUS_N = 0 # 0 or 1 or 2. Change this to yours
i2c = I2C(BUS_N)

# First write and read rapidly
read_data = i2c.writeread(ADDR, WRITE0)

# These also work
read_data = i2c.writeread(ADDR, [WRITE0, WRITE1])
read_data = i2c.writeread(ADDR, [WRITE0, WRITE1], bytes_n)
```



## 3. How to use useful functions? (Example)
### 3.1 `getBit`
```
from pyi2c import getBit

byte = 0x5a
print( bin(byte) )
# Will return '0b1011010'

print( getBit(byte, 0) )
# Will return 0 from #0 bit

print( getBit(byte, 1) )
# Will return 1 from #1 bit

if getBit(byte, 4) == 1:
    print('hoge')
# Will return 'hoge'
```



## 4. API
### 4.1 `I2C`
- `write`
- `read`
- `writeread`

### 4.2 Useful functions
- `getBit(byte, bit_n)`


## For developers
### Build
```
python3 -m build
```

### Upload
```
python3 -m twine upload dist/*
```



## Reference
- [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)
- [smbus2 GitHub](https://github.com/kplindegaard/smbus2)
- [Pure Python I2C : access to I2C components through serial or parallel interface.](http://pyi2c.sourceforge.net/)
