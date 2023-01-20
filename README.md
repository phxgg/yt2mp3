# YouTube To MP3 API

Simple API to convert YouTube videos and serving them as downloadable MP3 files.

Coded in **Python 3.11.1**

## Installation

1. Install requirements:
```
pip install -r requirements.txt
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

```
GET /info?url=https://www.youtube.com/watch?v=UsR08cY8k0A
```

**Response:**

```json
{
  "title": "JVKE - Golden Hour (Official Lyric Video)",
  [...]
}
```

### GET /download

Download a YouTube video as an MP3 file.

**Parameters:**

| Name | Type | Description |
| ---- | ---- | ----------- |
| url | string | YouTube video URL |

**Example:**

```
GET /download?url=https://www.youtube.com/watch?v=UsR08cY8k0A
```

**Response:**

```
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
| url | string | YouTube video URL |

**Example:**

```
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
