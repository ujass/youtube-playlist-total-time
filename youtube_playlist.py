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

dotenv_path = os.path.join(os.getcwd(), '.env')
dotenv.load_dotenv(dotenv_path) 
api_key = os.environ.get('YT_API_KEY') 

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
"""
playlist_request = youtube.playlists().list(
    part='contentDetails, snippet',
    channelId=channelId
)  

playlist_response = playlist_request.execute() 

# playlist will be in the items. 
for items in playlist_response['items']:
    print('\n2. Youtube Playlist response = \n',items)

