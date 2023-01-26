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

def is_youtube_url(url):
  return re.match(r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$', url)

def is_mixcloud_url(url):
  return re.match(r'^(https?\:\/\/)?(www\.)?(mixcloud\.com)\/.+$', url)

def is_soundcloud_url(url):
  return re.match(r'^(https?\:\/\/)?(www\.)?(soundcloud\.com)\/.+$', url)

def is_valid_url(url):
  return is_youtube_url(url) or is_mixcloud_url(url) or is_soundcloud_url(url)
