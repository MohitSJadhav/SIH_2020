#from flask import Flask, render_template, request
import base64
import re
from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt
import statistics
from statistics import mode
import keras
import cv2
import os
import simpleaudio as sa
from playsound import playsound
from pydub import AudioSegment
from gtts import gTTS
from googletrans import Translator

from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
from werkzeug.utils import secure_filename
import json


os.environ['KERAS_BACKEND'] = 'theano'


model = keras.models.load_model("model/CNN.model")
CATEGORIES = ['circle','rectangle','triangle']

CATEGORIES = ['circle','rectangle','triangle']
language={'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az',
'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca',
'cebuano': 'ceb', 'chinese(simplified)': 'zh-CN', 'chinese(traditional)': 'zh-TW', 'corsican': 'co',
'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo',
'estonian': 'et', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka',
'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian_creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw',
'hebrew': 'he', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id',
'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jv', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km',
'kinyarwanda': 'rw', 'korean': 'ko', 'kurdish': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv',
'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml',
'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn', 'myanmar(burmese)': 'my', 'nepali': 'ne',
'norwegian': 'no', 'nyanja(chichewa)': 'ny', 'odia(oriya)': 'or', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl',
'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'scots_gaelic': 'gd',
'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala(sinhalese)': 'si', 'slovak': 'sk',
'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv',
'tagalog(filipino)': 'tl', 'tajik': 'tg', 'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'thai': 'th',
'turkish': 'tr', 'turkmen': 'tk', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz',
'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}

sou = {1:"Draw a circle",2:"Draw a square",3:"Draw a traingle"}




app = Flask(__name__, template_folder='templates',static_folder='static')


with open("config.json",'r') as c:
    params = json.load(c)["params"]

local_server = False
app = Flask(__name__)
app.secret_key = "mohit-secret"
app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = "465",
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail_user'],
    MAIL_PASSWORD = params['gmail_password']
)
app.config['UPLOAD_FOLDER'] = params['upload_location']


if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_uri']

db = SQLAlchemy(app)

class Contact(db.Model):
    '''
    serialno , name , email , phone_number , message , date
    '''
    #serialno = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(80), primary_key = True)
    email = db.Column(db.String(20), nullable = False)
    phone_number = db.Column(db.String(12), nullable = False)
    message = db.Column(db.String(120), nullable = False)
    #date = db.Column(db.String(12), nullable=True)

class Posts(db.Model):
    '''
    sno , title , slug , context , date
    '''
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), primary_key = False)
    tag_line = db.Column(db.String(80), primary_key=False)
    slug = db.Column(db.String(20), nullable = False)
    context = db.Column(db.String(200), nullable = False)
    img_name = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=True)


@app.route('/form.html',methods = ['GET','POST'])
def form_file():
    if request.method == 'POST':
        user_name = request.form.get('inputEmail')
        user_password = request.form.get('inputPassword')
        confirm_password = request.form.get('inputPassword1')
        if user_name == params['admin_user'] and user_password == params['admin_password'] and user_password == confirm_password:
            post = Posts.query.filter_by().all()
            return render_template('canvas1.html', params=params, post=post)
        else:
            return render_template('form.html', params=params)
    else:
        return render_template('form.html', params = params )


@app.route('/dashboard.html',methods = ['GET','POST'])
def dashboard():
    post = Posts.query.filter_by().all()
    return render_template('dashboard.html',params = params , post = post)


@app.route('/result.html',methods = ['GET','POST'])
def result():
    return render_template('result.html')


@app.route('/failed.html',methods = ['GET','POST'])
def failed():
    return render_template('failed.html')


@app.route('/audio',methods = ['GET','POST'])
def audio():
    global langg
    langg = request.form.get('langg')
    print("In lang",langg)
    return str("True")


@app.route('/audio_played', methods=['GET','POST'])
def audio_player():
    lang = request.form.get('language')
    numb = int(request.form.get('numb'))
    print(numb)
    if lang in language.keys():
        translator= Translator()
        translation = (translator.translate(text = sou[numb], dest = language[lang]))
        txt = translation.text
        lang = language[lang]
        myobj = gTTS(text=txt, lang=lang, slow=False)
        myobj.save("/home/mj/Desktop/welcome.wav")
        #wave_obj = sa.WaveObject.from_wave_file('/home/mj/Desktop/welcome.wav')
        print("before playing")
        playsound("/home/mj/Desktop/welcome.wav")
        #play_obj = wave_obj.play();
        #sound1 = AudioSegment.from_file("/home/mj/Desktop/Birds.wav")
        #sound2 = AudioSegment.from_file("/home/mj/Desktop/welcome.mp3")
        #combined = sound1.overlay(sound2)
        #combined.export("/home/mj/Desktop/sih/static/combined.wav", format='wav')
        return str("True")
    else:
        return str("False")


@app.route('/')
def login():
    return render_template('form.html',params=params)

def prepare(file):
    IMG_SIZE = 28
    img_array = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)


@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/redir')
def redir():
    return str("True")

def extract(audio_played):
    audio_played = audio_played.split("-")
    return audio_played[1]


@app.route('/classify', methods=['GET','POST'])
def classify():
    print("IN classify")
    #audio_played = request.form.get('teamData')
    #audio_played = extract(audio_played)
    data = request.form.get('imageBase64')
    data = data.replace('data:image/png;base64,', '')
    data = data.replace(' ', '+')
    with open('upload.png', 'wb') as fh:
        fh.write(base64.b64decode(data))
    image = Image.open(r"upload.png")


    new_img = Image.new("RGB", (image.size[0],image.size[1]), (255, 255, 255))
    cmp_img = Image.composite(image, new_img, image).quantize(colors=256, method=2)
    cmp_img.save("/home/mj/Desktop/sih/Destination_path.png")
    image=Image.open('/home/mj/Desktop/sih/Destination_path.png')
    imageBox = image.getbbox()
    cropped=image.crop((imageBox[0]-10,imageBox[1]-10,imageBox[2]+10,imageBox[3]+10))
    cropped.save('/home/mj/Desktop/sih/pic.png')


    image = "/home/mj/Desktop/sih/pic.png" #your image path
    image = prepare(image)
    prediction = model.predict([image])
    prediction = list(prediction[0])
    shape_recognized = CATEGORIES[prediction.index(max(prediction))]
    print(shape_recognized)
    print(langg)
    if langg == shape_recognized:
        playsound("/home/mj/Desktop/sih/static/authentication_sucessfull.wav")
        return str("True")
    playsound("/home/mj/Desktop/sih/static/authentication_failed.wav")

    return str("False")




if __name__ == "__main__":
    app.run(host = "127.0.0.1",port = "9600",debug = True)
