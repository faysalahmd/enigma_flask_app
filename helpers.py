
# Gets settings from form and iunits the settings structure
def get_settings_from_request(request):
    r1_type = request.form['R1_type']
    r2_type = request.form['R2_type']
    r3_type = request.form['R3_type']
    r1_ring = int(request.form['R1_ring'])
    r2_ring = int(request.form['R2_ring'])
    r3_ring = int(request.form['R3_ring'])
    r1_init_pos = int(request.form['r1_init_position'])
    r2_init_pos = int(request.form['r2_init_position'])
    r3_init_pos = int(request.form['r3_init_position'])
    r3_turnover = request.form['r3_turnover']
    r2_turnover = request.form['r2_turnover']
    r1_turnover = request.form['r1_turnover']
    ukw = request.form['UKW']
    plug_board = request.form['plugboard_data'].strip()

    settings = {
        'RotorSettings':
            [
                {'RingType': r1_type, 'turnover': r1_turnover, 'start_offset': r1_init_pos, 'ring_setting': r1_ring},
                {'RingType': r2_type, 'turnover': r2_turnover, 'start_offset': r2_init_pos, 'ring_setting': r2_ring},
                {'RingType': r3_type, 'turnover': r3_turnover, 'start_offset': r3_init_pos, 'ring_setting': r3_ring},
            ],
        'UKW': ukw,
        'PlugBoard': plug_board
    }
    return settings



def convert_settings_list_to_dict(settings):
    settings_dict = dict()

    settings_dict['r1_type'] = settings[0]
    settings_dict['r2_type'] = settings[4]
    settings_dict['r3_type'] = settings[8]

    settings_dict['r1_turnover'] = settings[1]
    settings_dict['r2_turnover'] = settings[5]
    settings_dict['r3_turnover'] = settings[9]

    settings_dict['r1_init_pos'] = int(settings[2])
    settings_dict['r2_init_pos'] = int(settings[6])
    settings_dict['r3_init_pos'] = int(settings[10])

    settings_dict['r1_ring'] = settings[3]
    settings_dict['r2_ring'] = settings[7]
    settings_dict['r3_ring'] = settings[11]

    settings_dict['ukw'] = settings[12]
    settings_dict['plug_board'] = settings[13]

    return settings_dict


def convert_settings_to_str(settings):
    settings_str = ""
    for row in settings['RotorSettings']:
        settings_str += row['RingType'] + ','
        settings_str += str(row['turnover']) + ','
        settings_str += str(row['start_offset']) + ','
        settings_str += str(row['ring_setting']) + ','
    settings_str += settings['UKW']+','
    if settings['PlugBoard'] == "":
        settings_str += "AA"
    else:
        settings_str += settings['PlugBoard']
    print(settings_str)
    return settings_str
