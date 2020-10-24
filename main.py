from EnigmaMachine import EnigmaMachine
import pdb


settings = {
    'RotorSettings':
        [
            {'RingType': 'I', 'turnover': 'Q', 'start_offset': 0},
            {'RingType': 'II', 'turnover': 'E', 'start_offset': 0},
            {'RingType': 'III', 'turnover': 'E', 'start_offset': 0},
        ],
    'UKW': 'B',
    'PlugBoard': 'AZ BY CX DW EV FU GT HS IR JQ PP OO NN MM LL KK'
}

enigma = EnigmaMachine(settings)
print(enigma.encode('TESINGMYENIGMA'))
pdb.set_trace()
