import pdb
import numpy as np


class Rotor:

    # MODEL M3 Had 8 types of rotor settings.
    RING_SETTINGS = {
        'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
        'V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
        'VI': 'JPGVOUMFYQBENHZRDKASXLICTW',
        'VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
        'VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV',
    }

    def __init__(self, turnover_character, start_offset, ring_type, ring_setting):
        # Instance variables
        self.wheel = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.turnover_character = turnover_character

        self.rotor_ring = self.RING_SETTINGS[ring_type]
        self.update_rotor_settings(ring_setting)
        self.turn_rotor(start_offset)

    def update_rotor_settings(self, ring_setting):
        if ring_setting > 0:
            new_rotor_ring = ''
            for iter, letter in enumerate(self.rotor_ring):
                letter_ascii_num = ord(letter)
                if letter_ascii_num + ring_setting > 90:
                    letter_ascii_num = 64 + ((letter_ascii_num + ring_setting)-90)
                else:
                    letter_ascii_num += ring_setting

                shifted_letter = chr(letter_ascii_num)
                new_rotor_ring += shifted_letter
            self.rotor_ring = self.turn_rotor_right(ring_setting, list(new_rotor_ring))

    # Turns the Rotor by the given offset
    def turn_rotor(self, offset):
        if offset > len(self.rotor_ring):
            raise Exception("Invalid rotor shift offset.")

        self.rotor_ring = self.rotor_ring[offset:] + self.rotor_ring[:offset]
        self.wheel = self.wheel[offset:] + self.wheel[:offset]

    # Turns Rotor with Ring settings and alphabet offsets.
    def turn_rotor_right(self, offset, itemlist):
        shifted_list = np.roll(itemlist, offset)
        return ''.join(shifted_list)