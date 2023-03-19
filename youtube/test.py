import datetime
from pprint import pprint

from googleapiclient.errors import HttpError

from database_work import add_data_to_database
from main import youtube, check_has_referal_links
from url_work import get_links_from_text, define_sponsor

YOUTUBE_CHANNEL_ID = 'UCt7sv-NKh44rHAEb-qCCxvA'

start_date_str = "2022-02-20"
end_date_str = "2022-03-09"

# конвертируем даты в формат RFC 3339
start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").isoformat() + "Z"
end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").isoformat() + "Z"

def search_get():
    try:
        # делаем запрос на получение видео, указываем параметры publishedAfter и publishedBefore
        request = youtube.search().list(
            part="id",
            channelId=YOUTUBE_CHANNEL_ID,
            type="video",
            publishedAfter=start_date,
            publishedBefore=end_date,
            maxResults=50
        )
        response = request.execute()

        # обрабатываем полученный результат
        for item in response["items"]:
            video_id = item["id"]["videoId"]

            video_response = youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()

            description = video_response['items'][0]['snippet']['description']
            date = video_response['items'][0]['snippet']['publishedAt']
            link = f"https://www.youtube.com/watch?v={video_response['items'][0]['id']}"

            video_data = {
                'video_id': video_id,
                'description': description,
                'date': date,
                'link': link
            }
            print(date)
            check_has_referal_links(video_data)


    except HttpError as e:
        print("An error occurred: %s" % e)


if __name__ == '__main__':
    search_get()



