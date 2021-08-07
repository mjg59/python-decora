Python control for Leviton Decora Bluetooth switches
====================================================

A simple Python API for controlling [Leviton Decora switches](https://www.leviton.com/en/products/brands/decora-smart).

Example use
-----------

This will connect and turn on the light
```
import decora

switch = decora.decora("00:21:4d:00:00:01", key="key")
switch.connect()
switch.on()
```

This will set the light to 50% intensity
```
switch.set_brightness(50)
```

And turn the lights off
```
switch.off()
```

Obtaining the key
-----------------

Obtain the key by holding the down button on the switch until the green light flashes, and then run the get_key script.

**Noted on firmware 6.4**: `get_key.py` may not work on firmware version 6.4 as the key changing process is updated. However,
if you are able to get the key manually (e.g. from BLE sniffering), the library should still expect to work.
