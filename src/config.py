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

DEBUG_MODE = True
# SECRET_KEY = 'secret'