import requests
import feedparser
import os
from datetime import datetime
from time import mktime

def resolve_handle(handle):
    api_key = os.environ.get('YOUTUBE_API_KEY')
    clean_handle = handle.removeprefix('@')
    url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forHandle={clean_handle}&key={api_key}"
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    if data.get('items'):
        return data['items'][0]['id']
    return None

def fetch_videos(channel_id):
    # Convert standard Channel ID (UC...) to Long-Form Playlist ID (UULF...)
    if channel_id.startswith('UC'):
        playlist_id = 'UULF' + channel_id[2:]
    else:
        playlist_id = channel_id
    
    url = f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}"
    feed = feedparser.parse(url)
    
    videos = []
    for entry in feed.entries:
        videos.append({
            'id': entry.yt_videoid,
            'title': entry.title,
            'link': entry.link,
            'author': entry.author,
            # Parse time for sorting. (Note: UTC timezone by default from YouTube)
            'published_dt': datetime.fromtimestamp(mktime(entry.published_parsed)),
            'thumbnail': f"https://i.ytimg.com/vi/{entry.yt_videoid}/hqdefault.jpg"
        })
    return videos
