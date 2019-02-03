from flask import Flask, render_template, request, send_file,flash,redirect, url_for, send_from_directory,json
from facial.facifier import trigger
from werkzeug.utils import secure_filename
import os

from Geo.Geocoding import geocoder
from Geo.ReverseGeo import reverseGeo
from Geo.sitdist import caldist

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = 'upload/'
app.config['OUTPUT_FOLDER'] = 'output/'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/geo')
def geo ():
    return render_template('index.html')


@app.route('/facial')
def facial():
    return render_template('facial.html')

@app.route('/voice')
def voice():
    return render_template('voice.html')

@app.route('/dictionary')
def dictionary():
    return render_template('dictionary.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/about')
def about():
   return render_template('about.html')


@app.route('/distance')
def dist():
   return render_template('distance.html')



@app.route('/camera_stopped')
def stopped():
    return render_template("camera_page_stopped.html")

'''
@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    print(projectpath)
    return render_template("facial.html", projectpath=projectpath)
'''

@app.route('/trigger',  methods=['GET','POST'])
def invoke():
    firsttname = None
    if request.method == "POST":
        firsttname = request.get_json()
    print("First name = " + firsttname)

    trigger(firsttname)
    print("DONE....")

    return '{"hello": "world"}'

@app.route('/chat',  methods=['GET','POST'])
def chat():
    text = None
    if request.method == "POST":
        text = request.get_json()

        print("text received = " + text)

        jarvis_text="I am here to help you chat with your data."

    return json.dumps({'status':'OK','text':jarvis_text})

@app.route('/selectmenu', methods=['GET', 'POST'])
def selectmenu():
    if request.method == "POST":
        choice = request.form.get("choice", None)
        print(choice)
        if choice=='y':
            return render_template("new_user.html", choice = choice)
    return render_template("camera_page_started.html")

@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    if request.method == "POST":
        firsttname = request.form.get("firsttname", None)
        lasttname = request.form.get("lastname", None)
        print(firsttname)
        print(lasttname)
        return render_template("camera_page_started.html", firsttname=firsttname)

@app.route('/success-table',methods=['POST'])
def success():
    global filename
    if request.method=='POST':
        fil = request.files['file']
        filenames = []
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
        geocoder(fil,filename)
        filenames.append(filename)
        return render_template('upload.html', filenames=filenames)

@app.route('/table',methods=['GET','POST'])
def Caldist():
    if request.method=='POST':
        fil = request.files['file']
        range = request.form.get("range",None)
        print(range)

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            df= caldist(fil,range)
            print("outputfile is ",df)

@app.route('/upload', methods=['POST','GET'])
def upload():
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
            reverseGeo(filename)
    return render_template('upload.html', filenames=filenames)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file = "output_" + filename
    return send_from_directory(app.config['OUTPUT_FOLDER'],
                               file)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/reverse')
def reverse():
    return render_template("reverse.html")


@app.route('/download-table')
def download():
    return send_file('upload/format.zip',
                     mimetype='text/csv/zip',
                     attachment_filename='format.zip',
                     as_attachment=True)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)