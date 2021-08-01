"""
This is simple demo of how to connect with google apis. 

What we have done here? 
- We have created Youtube api key from google developer console and
    fetch the data from the youtube apis by the name of the youtube channel.

note:: never share env in git project.
"""

from googleapiclient.discovery import build
import os 
import dotenv

# Let us use the dot-env for better code stucture. 
dotenv_path = os.path.join(os.getcwd(), '.env')
dotenv.load_dotenv(dotenv_path)
# Always keep such key in environments and do not share environment with value with anyone.
api_key = os.environ.get('YT_API_KEY')


# make a build object 
youtube = build('youtube', 'v3', developerKey= api_key) 

# now create a request with this object. 
request = youtube.channels().list(
        part= 'contentDetails, statistics', 
        forUsername= 'sentdex'
    ) 

# execute this request and get response.
response = request.execute() 
print(response)
