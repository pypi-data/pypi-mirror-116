#!/bin/env python3
# -*- coding: utf-8 -*-
# pyi2c.py
"""
A useful I2C class and functions
"""
__author__      = "Eunchong Kim"
__copyright__   = "Copyright 2021, Eunchong Kim"
__credits__     = ["Eunchong Kim"]
__license__     = "GPL"
__version__     = "1.0.0"
__maintainer__  = "Eunchong Kim"
__email__       = "chariskimec@gmail.com"
__status__      = "Production"


# =================================================
# Require smbus2 to communicate
from smbus2 import SMBus, i2c_msg


# =================================================
class I2C:
    """
    A simple i2c interface by using smbus2, for Pi
    """
    def __init__(self, bus_n=0):
        self._bus = SMBus(bus_n)

    # Write data
    def write(self, addr, data):
        if not type(data) == list:
            data = [ data ]
        write_msg = i2c_msg.write(addr, data)
        self._bus.i2c_rdwr(write_msg)

    # Read bytes of data
    def read(self, addr, byte_size=1):
        read_msg = i2c_msg.read(addr, byte_size)
        self._bus.i2c_rdwr(read_msg)
        return list(read_msg)

    # Write data and read bytes of data soon
    def writeread(self, addr, data, byte_size):
        if not type(data) == list:
            data = [ data ]
        write_msg = i2c_msg.write(addr, data)
        read_msg = i2c_msg.read(addr, byte_size)
        self._bus.i2c_rdwr(write_msg, read_msg)
        return list(read_msg)


# =================================================
# Get bit in #n from the bytes data
def getBit(byte, bit_n):
    bit = 0 if byte & 2**bit_n == 0 else 1
    return bit


# =================================================
def main():
    pass


if __name__ == '__main__':
    main()
