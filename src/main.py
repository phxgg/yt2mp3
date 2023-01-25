import json
import os
import io
from contextlib import redirect_stdout

from flask import Flask, request, send_file, render_template, send_from_directory
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from yt_dlp import YoutubeDL
from utils import slugify, is_valid_url
from config import YDL_OPTIONS, HOST, PORT, DEBUG_MODE

SECRET_KEY = os.urandom(32)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY

csrf = CSRFProtect(app)
limiter = Limiter(app=app, key_func=get_remote_address)

@app.route('/robots.txt')
def static_from_root():
  return send_from_directory(app.static_folder, request.path[1:])

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

  with YoutubeDL(YDL_OPTIONS) as ydl:
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
@limiter.limit('500/day;50/hour;10/minute')
def download():
  # Get url from the request
  url = request.json.get('url')
  error = None

  # Check if url is empty
  if (url is None):
    error = 'URL is required'

  # Check if url is valid
  if (not is_valid_url(url)):
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
    with redirect_stdout(buffer), YoutubeDL(YDL_OPTIONS) as ydl:
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

@app.route('/', methods=['GET'])
@limiter.exempt
def index():
  # Get the URL from the request
  url = request.args.get('url')

  return render_template('index.html', host_url=request.host_url, url=url)

if __name__ == '__main__':
  app.run(host=HOST, port=PORT, debug=DEBUG_MODE)
