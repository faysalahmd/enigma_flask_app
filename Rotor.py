import pdb


class Rotor:

    wheel = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    turnover_character = 'Z'
    rotor_ring = []

    ring_settings = {
        'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
        'V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
        'VI': 'JPGVOUMFYQBENHZRDKASXLICTW',
        'VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
        'VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV',
    }

    def __init__(self, turnover_character, start_offset, ring_type):
        self.turnover_character = turnover_character
        self.rotor_ring = self.ring_settings[ring_type]
        self.turn_rotor(start_offset)

    # Turns the Rotor by the given offset
    def turn_rotor(self, offset):
        if offset > len(self.rotor_ring):
            raise Exception("Invalid rotor shift offset.")

        self.rotor_ring = self.rotor_ring[offset:] + self.rotor_ring[:offset]
        self.wheel = self.wheel[offset:] + self.wheel[:offset]


