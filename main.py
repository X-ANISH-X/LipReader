from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, jsonify
import os
from moviepy.editor import VideoFileClip

UPLOAD_FOLDER = 'static/videos'
lipReader = Flask(__name__)
lipReader.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
lipReader.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mkv', 'mov', 'mpg'}
lipReader.config['CONVERTED_FOLDER'] = 'converted'

if not os.path.exists(lipReader.config['UPLOAD_FOLDER']):
    os.makedirs(lipReader.config['UPLOAD_FOLDER'])

if not os.path.exists(lipReader.config['CONVERTED_FOLDER']):
    os.makedirs(lipReader.config['CONVERTED_FOLDER'])

@lipReader.route("/")
def home():
    return render_template("index.html")

@lipReader.route("/up")
def index():
    return render_template("index2.html")

@lipReader.route("/docs")
def docs():
    return render_template("docs.html")

@lipReader.route("/dnd")
def dnd():
    return render_template("dragndrop.html")

@lipReader.route('/upload1', methods=['POST'])
def upload_file1():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400
    if file and file.filename.lower().endswith('.mpg'):
        original_filename = file.filename
        filepath = os.path.join(lipReader.config['UPLOAD_FOLDER'], original_filename)
        file.save(filepath)

        mp4_filename = f"{os.path.splitext(original_filename)[0]}.mp4"
        mp4_filepath = os.path.join(lipReader.config['CONVERTED_FOLDER'], mp4_filename)

        # Convert MPG to MP4
        try:
            clip = VideoFileClip(filepath)
            clip.write_videofile(mp4_filepath, codec='libx264')
        except Exception as e:
            return jsonify(error=str(e)), 500

        return jsonify(filename=mp4_filename)
    else:
        return jsonify(error='Invalid file format'), 400

@lipReader.route('/uploads1/<filename>')
def uploaded_file(filename):
    return send_from_directory(lipReader.config['CONVERTED_FOLDER'], filename)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in lipReader.config['ALLOWED_EXTENSIONS']

@lipReader.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    # Inside the upload_file route
    if file and allowed_file(file.filename):
        filename = os.path.join(lipReader.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return render_template('index2.html', video_filename=file.filename)


@lipReader.route('/uploads/<filename>')
def serve_video(filename):
    return send_from_directory(lipReader.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    lipReader.run(debug=True)