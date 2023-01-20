import json
from flask import Flask, request, send_file
from yt_dlp import YoutubeDL
from contextlib import redirect_stdout
import io
import unicodedata
import re

def slugify(value, allow_unicode=False):
  """
  Taken from https://github.com/django/django/blob/master/django/utils/text.py
  Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
  dashes to single dashes. Remove characters that aren't alphanumerics,
  underscores, or hyphens. Convert to lowercase. Also strip leading and
  trailing whitespace, dashes, and underscores.
  """
  value = str(value)
  if allow_unicode:
    value = unicodedata.normalize('NFKC', value)
  else:
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
  value = re.sub(r'[^\w\s-]', '', value.lower())
  return re.sub(r'[-\s]+', '-', value).strip('-_')

app = Flask(__name__)

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

@app.route('/download', methods=['GET'])
def download():
  # Get the URL from the request
  url = request.args.get('url')

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

  response = app.response_class(
    response=f'<a href="{request.host_url}/download?url={url}">Click to Download</a>',
    status=200,
    mimetype='text/html'
  )
  return response

if __name__ == '__main__':
  app.run(debug=True)
