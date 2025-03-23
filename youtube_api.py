import os
from googleapiclient.discovery import build
from gooogleapplicant.errors import HttpError
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

class YouTubeAPI:
  def __init__(self):
    # Initialize YouTubeAPI Client
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
      raise ValueError('YOUTUBE_API_KEY is not set')
    
    self.youtube = build('youtube', 'v3', developerKey=api_key)

  def search_videos(self, query, max_results=50):
    # Search for videos based on query, return list of video IDs
    try:
      search_response = self.youtube.search().list(
        q=query,
        part='id',
        maxResults=max_results,
        type='video',
        relevanceLanguage='en'
      ).execute()

      video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
      return video_ids
    except HttpError as e:
      print(f"YouTubeAPI HTTP Error: {e}")
      return []
    except Exception as e:
      print(f"Error Searching YouTube: {e}")
      return []
    
  def get_video_details(self, video_ids):
    # Get Details for a list of video IDs
    if not video_ids:
      return []
    
    try:
      # YouTube API can only handle a maximum of 50 video IDs per request
      # Split video IDs into chunks of 50
      chunks = [video_ids[i:i+50] for i in range(0, len(video_ids), 50)]
      all_videos = []

      for chunk in chunks:
        videos_response = self.youtube.videos().list(
          part='snippet,statistics,contentDetails',
          id=','.join(chunk)
        ).execute()

        all_videos.extend(videos_response.get('items', []))

      return all_videos
    except HttpError as e:
      print(f"YouTubeAPI HTTP Error: {e}")
      return []
    except Exception as e:
      print(f"Error Getting Video Details: {e}")
      return []
    
  # Search for Specific Videos based on Subject, Subtopic, and Level
  # Returns Processed Video Details  
  def search_specific_videos(self, subject, subtopic='', level='beginner'):
    # Create Search Query
    search_query = f"{subject} {subtopic} {level} tutorial"
    search_query = search_query.strip()
