# Python module for control of Colorific bluetooth LED bulbs
#
# Copyright 2016 Matthew Garrett <mjg59@srcf.ucam.org>
#
# This code is released under the terms of the MIT license. See the LICENSE file
# for more details.

import sys

from bluepy import btle

class decoraException(Exception):
  pass

class decora:
  def __init__(self, mac, key=None):
    self.mac = mac
    if isinstance(key, str):
      self.key = int(key).to_bytes(4, byteorder='big')
    elif isinstance(key, int):
      self.key = key.to_bytes(4, byteorder='big')
    else:
      self.key = key

  def _connect(self):
    self.device = btle.Peripheral(self.mac, addrType=btle.ADDR_TYPE_PUBLIC)
    try:
      characteristics = self.device.getCharacteristics()
    except btle.BTLEException:
      raise decoraException("Unable to connect")
    self.handles = {}
    for characteristic in characteristics:
      if characteristic.uuid == "0000ff01-0000-1000-8000-00805f9b34fb":
        self.handles["state"] = characteristic.getHandle()
      if characteristic.uuid == "0000ff02-0000-1000-8000-00805f9b34fb":
        self.handles["config1"] = characteristic.getHandle()
      if characteristic.uuid == "0000ff03-0000-1000-8000-00805f9b34fb":
        self.handles["config2"] = characteristic.getHandle()
      if characteristic.uuid == "0000ff04-0000-1000-8000-00805f9b34fb":
        self.handles["location1"] = characteristic.getHandle()
      if characteristic.uuid == "0000ff05-0000-1000-8000-00805f9b34fb":
        self.handles["location2"] = characteristic.getHandle()
      if characteristic.uuid == "0000ff06-0000-1000-8000-00805f9b34fb":
        self.handles["event"] = characteristic.getHandle()
      if characteristic.uuid == "0000ff07-0000-1000-8000-00805f9b34fb":
        self.handles["time"] = characteristic.getHandle()
      if characteristic.uuid == "0000ff08-0000-1000-8000-00805f9b34fb":
        self.handles["data"] = characteristic.getHandle()
      if characteristic.uuid == "0000ff09-0000-1000-8000-00805f9b34fb":
        self.handles["name"] = characteristic.getHandle()

  def connect(self):
    self._connect()
    self.unlock()
    self.update_state()
    data = self.device.readCharacteristic(self.handles["config1"])
    self.bulbtype = data[0]
    self.maxoutput = data[1]
    self.minoutput = data[2]
    self.defaultoutput = data[3]
    data = self.device.readCharacteristic(self.handles["config2"])
    self.fadeon = data[0]
    self.fadeoff = data[1]
    self.ledtimeout = data[2]

  def read_key(self):
    self._connect()
    return self.get_event(83)[2:]

  def unlock(self):
    self.set_event(83, self.key)
    
  def update_state(self):
    data = self.device.readCharacteristic(self.handles["state"])
    self.power = data[0]
    self.level = data[1]

  def get_event(self, event):
    packet = bytearray([0x22, event, 0x00, 0x00, 0x00, 0x00])
    try:
      self.device.writeCharacteristic(self.handles["event"], packet, withResponse=True)
      return self.device.readCharacteristic(self.handles["event"])
    except btle.BTLEException:
      raise decoraException("Unable to get event")

  def set_event(self, event, data):
    packet = bytearray([0x11, event, data[0], data[1], data[2], data[3]])
    try:
      self.device.writeCharacteristic(self.handles["event"], packet, withResponse=True)
    except btle.BTLEException:
      raise decoraException("Unable to set event")

  def set_state(self):
    packet = bytearray([self.power, self.level])
    try:
      self.device.writeCharacteristic(self.handles["state"], packet, withResponse=True)
    except btle.BTLEException:
      raise decoraException("Unable to set state")

  def off(self):
    self.update_state()
    self.power = 0
    self.set_state()

  def on(self):
    self.update_state()
    self.power = 1
    self.set_state()

  def get_on(self):
    self.update_state()
    return self.power

  def set_brightness(self, level):
    self.update_state()
    self.level = level
    self.set_state()

  def get_brightness(self):
    self.update_state()
    return self.level
