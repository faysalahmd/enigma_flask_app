import pdb

def get_key(val):
    for key, value in plug_board.items():
        if val == value:
            return key

    raise Exception("invalid offset")

plug_board = {'A': 'Z',
              'B': 'Y',
              'C': 'X',
              'D': 'W',
              'E': 'V',
              'F': 'U',
              'G': 'T',
              'H': 'S',
              'I': 'R',
              'J': 'Q',
              'P': 'P',
              'O': 'O',
              'N': 'N',
              'M': 'M',
              'L': 'L',
              'K': 'K',
              }

def setup_rotor_initial_position(rotor, shift):
    assert shift < len(rotor)
    return rotor[shift:] + rotor[:shift]


ring_settings = [
                 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
                 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
                 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
                 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
                 'VZBRGITYUPSDNHLXAWMJQOFECK',
                 'JPGVOUMFYQBENHZRDKASXLICTW',
                 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
                 'FKQHTLXOCBJSPDZRAMEWNIUYGV',
                 ]

rotor_one = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
rotor_two = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
rotor_three = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

ETW = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
UKW_B = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'

input_str = "TESINGMYENIGMA"
output = []
for letter in input_str:

    if rotor_two[0] == 'E':
        rotor_three = setup_rotor_initial_position(rotor_three, 1)
        ring_settings[2] = setup_rotor_initial_position(ring_settings[2], 1)

    if rotor_one[0] == 'Q':
        rotor_two = setup_rotor_initial_position(rotor_two, 1)
        ring_settings[1] = setup_rotor_initial_position(ring_settings[1], 1)

    rotor_one = setup_rotor_initial_position(rotor_one, 1)
    ring_settings[0] = setup_rotor_initial_position(ring_settings[0], 1)

    try:
        plug_board_output = get_key(letter)
    except:
        plug_board_output = plug_board[letter]

    print("PlugBoard: " + plug_board_output)

    rotor_one_input = rotor_one[ETW.index(plug_board_output)]
    print("Rotor 1 Input : " + rotor_one_input)
    rotor_one_output = ring_settings[0][rotor_one.index(rotor_one_input)]
    print("Rotor 1 Output: " + rotor_one_output)



    rotor_two_input = rotor_two[rotor_one.index(rotor_one_output)]
    print("Rotor 2 Input: " + rotor_two_input)
    rotor_two_output = ring_settings[1][rotor_two.index(rotor_two_input)]
    print("Rotor 2 Output: " + rotor_two_output)

    rotor_three_input = rotor_three[rotor_two.index(rotor_two_output)]
    print("Rotor 3 Input: " + rotor_three_input)
    rotor_three_output = ring_settings[2][rotor_three.index(rotor_three_input)]
    print("Rotor 3 Output: " + rotor_three_output)

    reflector_output = UKW_B[rotor_three.index(rotor_three_output)]
    print("Reflector Input: " + rotor_three_output)
    print("Reflector Output: " + reflector_output)

    # reversed cycle

    rotor_3_r_input = rotor_three[rotor_three.index(reflector_output)]
    print("Rotor 3 reverse Output : " + rotor_3_r_input)
    rotor_3_r_output = rotor_three[ring_settings[2].index(rotor_3_r_input)]
    print("Rotor 3 reverse Intput: " + rotor_3_r_output)

    rotor_2_r_input = rotor_two[rotor_three.index(rotor_3_r_output)]
    print("Rotor 2 reverse Output : " + rotor_2_r_input)
    rotor_2_r_output = rotor_two[ring_settings[1].index(rotor_2_r_input)]
    print("Rotor 2 reverse Intput: " + rotor_2_r_output)

    rotor_1_r_input = rotor_one[rotor_two.index(rotor_2_r_output)]
    print("Rotor 1 reverse Output : " + rotor_1_r_input)
    rotor_1_r_output = rotor_one[ring_settings[0].index(rotor_1_r_input)]
    print("Rotor 1 reverse Intput: " + rotor_1_r_output)

    etw_r_input = ETW[rotor_one.index(rotor_1_r_output)]
    print("ETW reverse Intput: " + etw_r_input)
    etw_r_output = etw_r_input
    print("ETW reverse output: " + etw_r_output)

    plug_board_input = etw_r_output
    print("Plug Intput: " + plug_board_input)
    try:
        plug_board_output = get_key(plug_board_input)
    except:
        plug_board_output = plug_board[plug_board_input]
    print("Plug ouput: " + plug_board_output)
    print(plug_board_output)
    output.append(plug_board_output)

print(output)
pdb.set_trace()