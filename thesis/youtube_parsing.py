import sys
from datetime import datetime
from datetime import timedelta

import django
from googleapiclient.discovery import  build

sys.path.append('/Users/alexandrurustin/Desktop/thesis/thesis/thesis')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thesis.settings")
django.setup()

from funfly.models import Youtube

DEVELOPER_KEY = "AIzaSyB1dJ9YC6wkueu8q3M9d4HpRUP_BKIS9Oo"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

hours_to_subtract = 24
now = datetime.utcnow()
ago = timedelta(hours=-hours_to_subtract)
hours_ago = now + ago
hours_ago = str(hours_ago).replace(" ", "T")
hours_ago = hours_ago[:hours_ago.find(".")] + "Z"

def youtube_search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults = 20,
        order='viewCount',
        videoEmbeddable='true',
        type='video',
        publishedAfter=hours_ago,
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                       search_result["id"]["videoId"]))
            youtube_id = search_result["id"]["videoId"]
            youtube_title = search_result["snippet"]["title"]
            youtube_url = 'https://www.youtube.com/embed/' + youtube_id
            youtube_added_at = search_result["snippet"]["publishedAt"]
            description = search_result["snippet"]["description"]
            youtube_item = Youtube.objects.get_or_create(identifier=youtube_id, title=youtube_title,
                                                         date_added=youtube_added_at, url=youtube_url)


    print "Videos:\n", "\n".join(videos), "\n"

    return videos

if __name__ == '__main__':
    youtube_search('funny')