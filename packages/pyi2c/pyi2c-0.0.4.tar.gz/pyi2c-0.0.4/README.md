# A useful i2c Python3 package for Pi
It is a simple I2C interface based on smbus2.



## 1. Installation
Via [pip](https://pypi.org/project/pyi2c/)
```
pip3 install pyi2c
```



## 2. API and example
### 2.1 I2C
#### 2.1.1 declare
```
from pyi2c import I2C

# Create i2c
BUS_N = 0 # 0 or 1 or 2. Change this to yours
i2c = I2C(BUS_N)

ADDR = 0x38 # Change this to yours
```

#### 2.1.2 `write(ADDR, data)`
- `data` can be a byte or list of bytes.
```
WRITE0 = 0x00 # Change this to yours
i2c.write(ADDR, WRITE0)

# or write multi bytes, up to 64 bytes
WRITE1 = 0x01 # Change this to yours
i2c.write(ADDR, [WRITE0, WRITE1])
```

#### 2.1.2 `read(ADDR, byte_size)`
- `byte_size` can be empty (default is 1)
```
read_data = i2c.read(ADDR)

# or set length of reading bytes
byte_size = 2
read_data = i2c.read(ADDR, byte_size)
print( len(read_data) )
# 2
```

#### 2.1.3 `writeread(ADDR, data, byte_size)`
- `data` can be a byte or list of bytes.
- `byte_size` can be empty (default is 1)
```
# First write and read rapidly one byte
read_data = i2c.writeread(ADDR, WRITE0)

# These also work
read_data = i2c.writeread(ADDR, [WRITE0, WRITE1])
read_data = i2c.writeread(ADDR, [WRITE0, WRITE1], byte_size)
```



### 2.2 `getBit(byte, bin_n, bin_m=-1)`
```
from pyi2c import getBit

byte = 0x5a # Any byte data
print( bin(byte) )
# '0b1011010'
```

- Get bit #n of byte
```
print( getBit(byte, 0) )
# 0

print( getBit(byte, 1) )
# 1
```

- Get multi bits from #n to #m of byte
```
print( getBit(byte, 4, 3) )
# 3 = 0b10
print( getBit(byte, 3, 4) )
# 3 = 0b10, the same as previous

```

- Recommen usage
```
if getBit(byte, 4) == 0b1:
    print('hoge')
# 'hoge'
```



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
