from flask import Flask, request, render_template, Response, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, AUDIO
import sys, os
import speech_recognition as sr
import cv2

# import audio_transcribe as audio

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
global camera
camera=cv2.VideoCapture(0)



@app.route("/")
def index():
    return render_template("index.html", error = "")

@app.route('/submit', methods=['POST'])
def submit():
    global error, songs, filename, result_file
    print("filename " + filename)
    changed_text = request.form['text']
    result_file = "result/" + filename
    print("result file is " +result_file)
    f = open(result_file,'w')
    f.write('Recognition is:\n')
    f.write(changed_text)
    f.close()
    return render_template('index.html', error = changed_text, songs = songs)

@app.route('/calc')
def calc():
     return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

def get_frame():
    global camera

    ramp_frames=100

    i=1
    while True:
        global im
        retval, im = camera.read()
        imgencode=cv2.imencode('.jpg',im)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i+=1

    del(camera)

@app.route('/save_photo')
def save_photo():
    global camera, im
    im = camera.read()[1]
    target = os.path.join(APP_ROOT, 'static/')
    if not os.path.isdir(target):
        os.mkdir(target)
    for name in os.listdir(target):
        print(name)
    new_count = len([name for name in os.listdir(target)])
    print("new_count" + str(new_count))
    filename = "static/im" + str(new_count)  + ".jpg"
    cv2.imwrite(filename = filename, img=im)
    return redirect(url_for('index'))


if __name__ == "__main__":
    global error, songs, filename, result_file
    error = ""
    songs = ""
    filename = ""
    result_file = ""
    app.run(host="143.215.86.253",port=4555, debug=True)
