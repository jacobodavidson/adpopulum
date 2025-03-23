# test_api.py
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os

load_dotenv()

def test_youtube_api():
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("ERROR: YouTube API key not found in .env file")
        return False
    
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Simple request to test API key
        request = youtube.search().list(
            part="snippet",
            maxResults=1,
            q="test"
        )
        response = request.execute()
        
        print("YouTube API connection successful!")
        print("Sample response:")
        print(response)
        return True
    except HttpError as e:
        print(f"YouTube API Error: {e}")
        if "quota" in str(e).lower():
            print("This might be a quota issue. Check your Google Cloud Console to see if you've exceeded your daily quota.")
        elif "invalid" in str(e).lower():
            print("This might be an invalid API key. Verify your key in the Google Cloud Console.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_youtube_api()