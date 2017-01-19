#!/usr/bin/python

import decora
import sys

address = sys.argv[1]
switch = decora.decora(address, None)
rawkey = switch.read_key()
if rawkey == "LEVI":
    print("Switch is not in pairing mode - hold down until green light flashes\n")
else:
    key = int(ord(rawkey[0])) << 24 | int(ord(rawkey[1])) << 16 | int(ord(rawkey[2])) << 8 | int(ord(rawkey[3]))
    print(hex(key))
