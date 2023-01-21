# Do not edit this variable if you don't know what you are doing
YDL_OPTIONS = {
  'outtmpl': '-',
  'logtostderr': True,
  'format': 'm4a/bestaudio/best',
  'postprocessors': [{  # Extract audio using ffmpeg
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
  }]
}

HOST = '127.0.0.1'
PORT = 5000
DEBUG_MODE = True
# SECRET_KEY = 'secret'
