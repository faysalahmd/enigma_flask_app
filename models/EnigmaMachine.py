from models.Rotor import Rotor

'''
 Enigma Model M3 with Turnover points R1 : Q, R2 : E, R3 : E. Fixed 8 Rotor Types.
'''


class EnigmaMachine:

    ETW = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Constructors takes the settings and initiates the enigma machine (Rotors, PlugBoard, Reflector (UKW), ETW)
    def __init__(self, settings):
        self.plug_board = {}
        self.rotors = []
        self.UKW = ''

        self.init_plug_board(settings['PlugBoard'])
        self.set_ukw(settings['UKW'])
        self.init_rotors(settings['RotorSettings'])
        self.rotor_1 = self.rotors[0]
        self.rotor_2 = self.rotors[1]
        self.rotor_3 = self.rotors[2]

    def init_rotors(self, rotor_settings):
        for rotor_setting in rotor_settings:
            rotor = Rotor(rotor_setting['turnover'], rotor_setting['start_offset'], rotor_setting['RingType'],
                          rotor_setting['ring_setting'])
            self.rotors.append(rotor)

    def set_ukw(self, ukw_type):
        if ukw_type == 'B':
            self.UKW = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
        elif ukw_type == 'C':
            self.UKW = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
        else:
            raise Exception("Invalid UKW Type specified.")

    def init_plug_board(self, plug_board_string):
        if len(plug_board_string) >= 2:
            plug_combinations = plug_board_string.split(' ')
            for combo in plug_combinations:
                self.plug_board[combo[0]] = combo[1]

    def get_plug_board_output(self, input):
        try:
            # Get from values
            return self.plug_board[input]
        except Exception as e:
            # Get from keys
            for key, value in self.plug_board.items():
                if input == value:
                    return key
            # Does not exist in board, so no bounding
            return input

    # Runs the input string through enigma machine and returns encoded string.
    def encode(self, plain_string):
        output = []

        # TODO : I CAN IMPROVE THE FOR LOOP FURTHER WITH LESS STATEMENTS AND ONE DYNAMIC METHOD CALL
        #  FOR EACH ROTOR, ran out of time for now.

        for letter in plain_string:
            # Turn Rotors
            self.turn_rotors()

            # Get letter from the plug board
            plug_output = self.get_plug_board_output(letter)

            # Pass through rotors and back
            rotors_output = self.cycle_through_rotors(plug_output)

            # Pass reversed through ECW To Plug Board
            etw_r_input = self.ETW[self.rotor_1.wheel.index(rotors_output)]
            etw_r_output = etw_r_input
            plug_output = self.get_plug_board_output(etw_r_output)
            output.append(plug_output)
        return ''.join(output)

    # Passes the input through ROTOR 1 , ROTOR 2 , ROTOR 3 and back
    def cycle_through_rotors(self, input):
        rotor_1_input = self.rotor_1.wheel[self.ETW.index(input)]
        rotor_1_output = self.rotor_1.rotor_ring[self.rotor_1.wheel.index(rotor_1_input)]

        # Pass through Rotor 2
        rotor_2_input = self.rotor_2.wheel[self.rotor_1.wheel.index(rotor_1_output)]
        rotor_2_output = self.rotor_2.rotor_ring[self.rotor_2.wheel.index(rotor_2_input)]

        # Pass through Rotor 3
        rotor_3_input = self.rotor_3.wheel[self.rotor_2.wheel.index(rotor_2_output)]
        rotor_3_output = self.rotor_3.rotor_ring[self.rotor_3.wheel.index(rotor_3_input)]

        # Reflect Back to rotors
        reflector_output = self.UKW[self.rotor_3.wheel.index(rotor_3_output)]

        # Reversed Cycle
        # Pass reversed through Rotor 3
        rotor_3_r_input = self.rotor_3.wheel[self.rotor_3.wheel.index(reflector_output)]
        rotor_3_r_output = self.rotor_3.wheel[self.rotor_3.rotor_ring.index(rotor_3_r_input)]

        # Pass reversed through Rotor 2
        rotor_2_r_input = self.rotor_2.wheel[self.rotor_3.wheel.index(rotor_3_r_output)]
        rotor_2_r_output = self.rotor_2.wheel[self.rotor_2.rotor_ring.index(rotor_2_r_input)]

        # Pass reversed through Rotor 1
        rotor_1_r_input = self.rotor_1.wheel[self.rotor_2.wheel.index(rotor_2_r_output)]
        return self.rotor_1.wheel[self.rotor_1.rotor_ring.index(rotor_1_r_input)]

    def turn_rotors(self):
        # Rotor 2 Turning Checks
        if self.rotor_1.wheel[0] == self.rotor_1.turnover_character:
            self.rotor_2.turn_rotor(1)

        # Rotor 3 turning Check
        if self.rotor_2.wheel[0] == self.rotor_2.turnover_character:
            self.rotor_3.turn_rotor(1)
        self.rotor_1.turn_rotor(1)