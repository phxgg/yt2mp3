# YouTube To MP3 Converter

Simple web app that converts YouTube videos and serves them as downloadable MP3 files.

Coded in **Python 3.11.1**

## Installation

1. Install requirements:
```
pip install -r requirements.txt
```

You will also need to have **ffmpeg** installed on your system.

```bash
# Ubuntu
sudo apt install ffmpeg

# Homebrew macOS
brew install ffmpeg

# Windows
# Download the latest version from https://ffmpeg.org/download.html
# Extract the archive and add the bin folder to your PATH
```

2. Run the server:
```
python main.py
```

## Endpoints

### GET /info

Get information about a YouTube video.

**Parameters:**

| Name | Type | Description |
| ---- | ---- | ----------- |
| url | string | YouTube video URL |

**Example:**

```http
GET /info?url=https://www.youtube.com/watch?v=UsR08cY8k0A
```

**Response:**

```json
{
  "title": "JVKE - Golden Hour (Official Lyric Video)",
  [...]
}
```

### POST /download

Download a YouTube video as an MP3 file.

> **Note:**
> This endpoint is CSRF protected. You will need to send a CSRF token in the `X-CSRFToken` header.

**Parameters:**

| Name | Type | Description |
| ---- | ---- | ----------- |
| `url` | `string` | YouTube video URL |

Content-Type: `application/json`

**Response:**

```http
HTTP/1.1 200 OK
Content-Disposition: attachment; filename=jvke-golden-hour-official-lyric-video.mp3
Content-Length: 3502304
Content-Type: audio/mpeg
```

### GET /get_download_url

> **Warning:**
> Under development.

Grabs an audio only URL from a YouTube video.

**Parameters:**

| Name | Type | Description |
| ---- | ---- | ----------- |
| `url` | `string` | YouTube video URL |

**Example:**

```http
GET /get_download_url?url=https://www.youtube.com/watch?v=UsR08cY8k0A
```

**Response:**

```json
{
  "title": "JVKE - golden hour (Official Lyric Video)",
  "video_id": "UsR08cY8k0A",
  "download_url": "<a_youtube_audio_url>"
}
```
