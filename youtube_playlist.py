"""
This is the main file where we find the total time of the youtube playlist. 
For that, we need to do these floowing things. 

1. Get youttube developer key. 
2. make a query to find user id from channel name. 
3. find the play list. 

"""

from googleapiclient.discovery import build
import os 
import dotenv
import re 
from datetime import timedelta

dotenv_path = os.path.join(os.getcwd(), '.env')
dotenv.load_dotenv(dotenv_path) 
api_key = os.environ.get('YT_API_KEY') 

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

"""
1. Find the channel ID from the user name. 
"""
youtube = build('youtube', 'v3', developerKey= api_key) 
request = youtube.channels().list(
        part= 'contentDetails, statistics', 
        forUsername= 'sentdex'
    ) 

response = request.execute() 
print('\n1. Youtube channerId response = \n',response)     

channelId = response['items'][0]['id']
print(channelId) 

"""
2. Now let's do the playlist request. 
Below, this we find the content of the channel with the channel id. 
"""
playlist_request = youtube.playlists().list(
    part='contentDetails',
    channelId=channelId
)  

playlist_response = playlist_request.execute() 

# playlist will be in the items. 
for items in playlist_response['items']:
    print('\n2. Youtube Playlist response = \n',items)
    playlist_id = items['id']

print("\nlast playlist id we fetch = {}".format(playlist_id))

"""
Playlist id ---> Video seconds.

Now we have playlist id, lets us fetch the content (vidoes) of the playlist. 
Below, we have find the content of the playlist with the playlist id. 

Note: we can fetch max 50 results per request.
Need: Playlist id.
Get: Video id.
"""
nextPageToken = None 
totalSeconds = 0 
while True:
    playlist_videos_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=nextPageToken

    )

    playlist_videos_response = playlist_videos_request.execute() 

    video_id_list = []
    for item in playlist_videos_response['items']:
        video_id_list.append(item['contentDetails']['videoId'])

    print(",".join(video_id_list)) 

    """
    We have video list.
    Now, we want video details. 

    need: Video ids
    Get: Video details, video duration

    TO pares the duration, we also need to define the regular expression. 
    """ 



    video_details = youtube.videos().list(
        part='contentDetails',
        id=','.join(video_id_list)
    ) 

    video_response = video_details.execute() 

    for item in video_response['items']:
        duration = item['contentDetails']['duration']

        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        hours = int(hours.group(1)) if hours else 0 
        minutes = int(minutes.group(1)) if minutes else 0 
        seconds = int(seconds.group(1)) if seconds else 0 

        video_seconds = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        ).total_seconds()

        totalSeconds += video_seconds
    nextPageToken = playlist_videos_response.get('nextPageToken')

    if not nextPageToken:
        break 

totalSeconds = int(totalSeconds)
print(f'total seconds= {totalSeconds}') 

minutes, seconds = divmod(totalSeconds,60)
hours, minutes = divmod(minutes, 60) 

print(f'{hours}:{minutes}:{seconds}')