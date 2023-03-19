from datetime import datetime
from pprint import pprint

from googleapiclient.discovery import build
import csv
from url_work import *
from database_work import *

CREDENTIALS = "AIzaSyDhXYTqFu8gnhakdR-bsdxq-uVKgfW5QBo"
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YOUTUBE_CHANNEL_ID = 'UCt7sv-NKh44rHAEb-qCCxvA'

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=CREDENTIALS
)

start_date_str = "2021-01-01"
end_date_str = "2022-03-15"

# конвертируем даты в формат RFC 3339
start_date = datetime.strptime(start_date_str, "%Y-%m-%d").isoformat() + "Z"
end_date = datetime.strptime(end_date_str, "%Y-%m-%d").isoformat() + "Z"

def get_channel_videos(channel_id):
    res = youtube.channels().list(id=channel_id,
                                  part="snippet,contentDetails").execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None

    while 1:
        res = youtube.playlistItems().list(playlistId=playlist_id,
                                           part="snippet,contentDetails",
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        for item in res['items']:
            video_date = item['snippet']['publishedAt']
            k = datetime.strptime(video_date, "%Y-%m-%dT%H:%M:%SZ")
            if start_date < k < end_date:
                video_data = {
                    'video_id': item['contentDetails']['videoId'],
                    'description': item['snippet']['description'],
                    'date': item['snippet']['publishedAt'],
                    'link': f"https://www.youtube.com/watch?v={item['contentDetails']['videoId']}"
                }
                check_has_referal_links(video_data)

        next_page_token = res.get('nextPageToken')
        if next_page_token is None:
            break
    return


def check_has_referal_links(json):
    ref_link = get_links_from_text(json['description'])
    if len(ref_link) == 0:
        return
    whois_info = define_sponsor(ref_link)

    video_characteristics = youtube.videos().list(
        id=json['video_id'],
        part="statistics,contentDetails"
    )

    response_statistics = video_characteristics.execute()

    views_number = int(response_statistics['items'][0]['statistics']['viewCount'])
    likes_number = int(response_statistics['items'][0]['statistics']['likeCount'])
    duration = response_statistics['items'][0]['contentDetails']['duration']
    comments_number = int(response_statistics['items'][0]['statistics']['commentCount'])

    video_data = {
        'video_id': (json['video_id']),
        'description': (json['description']),
        'date': (json['date']),
        'link': (json['link']),
        'views': views_number,
        'likes': likes_number,
        'duration': duration,
        'comments_number': comments_number,
        'ref_link': ref_link,
        "whois_info": whois_info
    }
    print("Addded")
    add_data_to_database(video_data)


if __name__ == '__main__':
    get_channel_videos(YOUTUBE_CHANNEL_ID)
