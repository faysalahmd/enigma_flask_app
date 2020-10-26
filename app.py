import os
from flask import Flask, render_template, request, flash, redirect, session, url_for
from models.EnigmaMachine import EnigmaMachine
from models.ImageStegano import ImageStegano
import time
from helpers import *

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'imports')
ALLOWED_EXTENSIONS = (['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'


def upload_image(image_field, dir, request):

    if image_field not in request.files:
        flash('No file part')
        return False, ''

    file = request.files[image_field]
    if file.filename == '':
        flash('No selected file')
        return False, ''
    if file and allowed_file(file.filename):
        filename = str(time.time_ns()) + file.filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], dir, filename)
        file.save(image_path)
        return True, image_path
    else:
        flash("Invalid image format. JPG/PNG Only")
        return False, ''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/importSettings', methods=['POST'])
def import_settings():

    upload_status, file_name = upload_image('settings_image', 'settings', request)
    if upload_status:
        stagno = ImageStegano()
        decoded_binary = ''.join(stagno.decode(file_name))
        status, settings_data = stagno.checkdata(decoded_binary)
        settings_list = settings_data.split(",")
        if status and len(settings_list) == 14:
            settings_dict = convert_settings_list_to_dict(settings_list)

            session['r1_type'] = settings_dict['r1_type']
            session['r2_type'] = settings_dict['r2_type']
            session['r3_type'] = settings_dict['r3_type']

            session['r1_ring'] = settings_dict['r1_ring']
            session['r2_ring'] = settings_dict['r2_ring']
            session['r3_ring'] = settings_dict['r3_ring']

            session['r1_init_pos'] = int(settings_dict['r1_init_pos'])
            session['r2_init_pos'] = int(settings_dict['r2_init_pos'])
            session['r3_init_pos'] = int(settings_dict['r3_init_pos'])

            session['r1_turnover'] = settings_dict['r1_turnover']
            session['r2_turnover'] = settings_dict['r2_turnover']
            session['r3_turnover'] = settings_dict['r3_turnover']

            session['ukw'] = settings_dict['ukw']
            session['plug_board'] = settings_dict['plug_board']
        else:
            flash("Invalid settings data.")
    else:
        flash("Invalid image format. JPG/PNG Only")

    return redirect('/')

@app.route('/resetsettings', methods=['GET'])
def reset():
    session.clear()
    return redirect('/')


@app.route('/', methods=['POST'])
def index_post():
    settings = get_settings_from_request(request)
    input_string = ""
    print(settings)
    if request.form['input_format'] == 'str':
        input_string = (request.form['input_string']).upper()
    elif request.form['input_format'] == 'img':
        upload_status, file_name = upload_image('input_image', 'inputs', request)
        if upload_status:
            stagno = ImageStegano()
            decoded_binary = ''.join(stagno.decode(file_name))
            status, input_string = stagno.checkdata(decoded_binary)
            print("input_string")
            if not status:
                flash("Input image contains no encoded data in it.")
        else:
            flash("Invalid image format.")

    enigma = EnigmaMachine(settings)
    output = enigma.encode(input_string)
    print("output " + output)
    # If output is required in images, check/upload images.
    if request.form['enc_format'] == 'img':
        settings_image_status, setings_image = upload_image('setings_image', 'settings', request)
        data_image_status, data_image = upload_image('data_image', 'data', request)

        if not settings_image_status or not data_image_status:
            flash("Output images format should be PNG/JPG")
            return render_template('index.html')
        else:
            # Encode data in to images
            settings_str = convert_settings_to_str(settings)
            stagno = ImageStegano()
            try:
                encoded_settings_image_path = stagno.encode(setings_image, settings_str, "encoded")
                encoded_data_image_path = stagno.encode(data_image, output, "encoded")
                data = {
                    'data_image': encoded_data_image_path,
                    'setting_image': encoded_settings_image_path,
                }
                print(data)
                return render_template('index.html', img_data=data)
            except Exception as e:
                flash(str(e))
            return render_template('index.html')
    else:
        return render_template('index.html', data={'output': output})

app.run()
