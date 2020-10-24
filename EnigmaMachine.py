from Rotor import Rotor
import pdb


class EnigmaMachine:
    plug_board = {}
    ETW = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    UKW = ''
    rotors = []

    # Constructors takes the settings and initiates the enigma machine (Rotors, PlugBoard, Reflector (UKW), ETW)
    def __init__(self, settings):
        self.init_plug_board(settings['PlugBoard'])
        self.set_ukw(settings['UKW'])
        self.init_rotors(settings['RotorSettings'])

    def init_rotors(self, rotor_settings):
        for rotor_setting in rotor_settings:
            rotor = Rotor(rotor_setting['turnover'], rotor_setting['start_offset'], rotor_setting['RingType'])
            self.rotors.append(rotor)

    def set_ukw(self, ukw_type):
        if ukw_type == 'B':
            self.UKW = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
        elif ukw_type == 'C':
            self.UKW = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
        else:
            raise Exception("Invalid UKW Type specified.")

    def init_plug_board(self, plug_board_string):
        plug_combinations = plug_board_string.split(' ')

        for combo in plug_combinations:
            self.plug_board[combo[0]] = combo[1]

    def get_plug_board_output(self, input):
        for key, value in self.plug_board.items():
            if input == value:
                return key
        return self.plug_board[input]

    # Runs the characters of input string through Enigma Cycle and returns encoded string/list
    def encode(self, plain_string):
        rotor_1 = self.rotors[0]
        rotor_2 = self.rotors[1]
        rotor_3 = self.rotors[2]
        output = []
        for letter in plain_string:
            # Rotor 2 turning
            if rotor_1.wheel[0] == rotor_1.turnover_character:

                print(len(rotor_2.rotor_ring))
                rotor_2.turn_rotor(1)
                print(len(rotor_2.rotor_ring))

            # Rotor 3 turning
            if rotor_2.wheel[0] == rotor_2.turnover_character:
                rotor_3.turn_rotor(1)

            rotor_1.turn_rotor(1)

            # Get letter from the plug board
            plug_output = self.get_plug_board_output(letter)

            # Pass through ETC To Rotor 1
            rotor_1_input = rotor_1.wheel[self.ETW.index(plug_output)]
            rotor_1_output = rotor_1.rotor_ring[rotor_1.wheel.index(rotor_1_input)]

            # Pass through Rotor 2
            rotor_2_input = rotor_2.wheel[rotor_1.wheel.index(rotor_1_output)]
            rotor_2_output = rotor_2.rotor_ring[rotor_2.wheel.index(rotor_2_input)]

            # Pass through Rotor 3
            rotor_3_input = rotor_3.wheel[rotor_2.wheel.index(rotor_2_output)]
            rotor_3_output = rotor_3.rotor_ring[rotor_3.wheel.index(rotor_3_input)]

            # Reflect Back to rotors
            reflector_output = self.UKW[rotor_3.wheel.index(rotor_3_output)]

            # Reversed Cycle
            # Pass reversed through Rotor 3
            rotor_3_r_input = rotor_3.wheel[rotor_3.wheel.index(reflector_output)]
            rotor_3_r_output = rotor_3.wheel[rotor_3.rotor_ring.index(rotor_3_r_input)]

            # Pass reversed through Rotor 2
            rotor_2_r_input = rotor_2.wheel[rotor_3.wheel.index(rotor_3_r_output)]
            rotor_2_r_output = rotor_2.wheel[rotor_2.rotor_ring.index(rotor_2_r_input)]

            # Pass reversed through Rotor 1
            rotor_1_r_input = rotor_1.wheel[rotor_2.wheel.index(rotor_2_r_output)]
            rotor_1_r_output = rotor_1.wheel[rotor_1.rotor_ring.index(rotor_1_r_input)]

            # Pass reversed through ECW To Plug Board
            etw_r_input = self.ETW[rotor_1.wheel.index(rotor_1_r_output)]
            etw_r_output = etw_r_input

            plug_output = self.get_plug_board_output(etw_r_output)

            output.append(plug_output)

        return output

