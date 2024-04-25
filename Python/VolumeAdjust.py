"""
Script to adjust volume on the py; called from the main program.

@author jdeanes0
@version 4/25/24
"""

import alsaaudio
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--level')
args = parser.parse_args()

m = alsaaudio.Mixer()

try:
	new_volume = m.getvolume()[0] + int(args.level)
	m.setvolume(new_volume)
	print(f"Current Volume: {m.getvolume()}")
except alsaaudio.ALSAAudioError:
	print("Attempted volume is out of bounds")

