import json
from flask import Flask, request, send_file, render_template
from yt_dlp import YoutubeDL
from contextlib import redirect_stdout
import io
from utils import slugify, is_youtube_url
from flask_wtf.csrf import CSRFProtect
import os

SECRET_KEY = os.urandom(32)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)

ydl_opts = {
  'outtmpl': '-',
  'logtostderr': True,
  'format': 'm4a/bestaudio/best',
  'postprocessors': [{  # Extract audio using ffmpeg
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
  }]
}

@app.route('/', methods=['GET'])
def index():
  response = app.response_class(
    response=json.dumps({'message': 'Hello World!'}, indent=2),
    status=200,
    mimetype='application/json'
  )
  return response

@app.route('/info', methods=['GET'])
def info():
  # Get the URL from the request
  url = request.args.get('url')

  with YoutubeDL() as ydl:
    try:
      info_dict = ydl.extract_info(url, download=False)

      response = app.response_class(
        response=json.dumps(info_dict, indent=2),
        status=200,
        mimetype='application/json'
      )
      return response
    except Exception as e:
      response = app.response_class(
        response=json.dumps({'error': 'Something went wrong'}),
        status=500,
        mimetype='application/json'
      )
      return response

@app.route('/get_download_url', methods=['GET'])
def get_download_url():
  # Get the URL from the request
  url = request.args.get('url')

  with YoutubeDL(ydl_opts) as ydl:
    try:
      info_dict = ydl.extract_info(url, download=False)
      
      # Download and stream to the client
      response = app.response_class(
        response=json.dumps({
          'title': info_dict['title'],
          'video_id': info_dict['id'],
          'download_url': [item for item in info_dict['formats'] if item['format_id'] == '140'][0]['url']
        }, indent=2),
        status=200,
        mimetype='application/json'
      )
      return response
    except Exception as e:
      print(e)
      response = app.response_class(
        response=json.dumps({'error': 'Something went wrong'}),
        status=500,
        mimetype='application/json'
      )
      return response

@app.route('/download', methods=['POST'])
def download():
  # Get url from the request
  url = request.json.get('url')
  error = None

  # Check if url is empty
  if (url is None):
    error = 'URL is required'

  # Check if url is valid
  if (not is_youtube_url(url)):
    error = 'URL is not valid'
  
  if (error is not None):
    response = app.response_class(
      response=json.dumps({'error': error}),
      status=400,
      mimetype='application/json'
    )
    return response

  try:
    filename = ''

    buffer = io.BytesIO()
    with redirect_stdout(buffer), YoutubeDL(ydl_opts) as ydl:
      info_dict = ydl.extract_info(url, download=False)
      filename = slugify(info_dict['title']) + '.mp3'
      ydl.download([url])

    buffer.seek(0)
    return send_file(buffer, download_name=filename, as_attachment=True)
  except Exception as e:
    print(e)
    response = app.response_class(
      response=json.dumps({'error': 'Something went wrong'}),
      status=500,
      mimetype='application/json'
    )
    return response

@app.route('/convert', methods=['GET'])
def convert():
  # Get the URL from the request
  url = request.args.get('url')

  return render_template('convert.html', host_url=request.host_url, url=url)

if __name__ == '__main__':
  app.run(debug=True)
