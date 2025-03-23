import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
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

            video_ids = [
                item['id']['videoId']
                for item in search_response.get('items', [])
            ]
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
            chunks = [
                video_ids[i:i+50]
                for i in range(0, len(video_ids), 50)
            ]
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
    
    def search_specific_videos(self, subject, subtopic='', level='beginner'):
        # Create Search Query
        search_query = f"{subject} {subtopic} {level} tutorial".strip()

        # Search for Videos
        video_ids = self.search_videos(search_query)

        if not video_ids:
            return []
        
        # Get Video Details
        video_details = self.get_video_details(video_ids)

        processed_videos = []
        for video in video_details:
            try:
                processed_video = {
                    'id': video['id'],
                    'title': video['snippet']['title'],
                    'description': (
                        video['snippet']['description'][:200] + '...'
                        if len(video['snippet']['description']) > 200
                        else video['snippet']['description']
                    ),
                    'thumbnail': video['snippet']['thumbnails']['high']['url'],
                    'channel_title': video['snippet']['channelTitle'],
                    'published_at': video['snippet']['publishedAt'],
                    'view_count': int(video['statistics'].get('viewCount', 0)),
                    'like_count': int(video['statistics'].get('likeCount', 0)),
                    'comment_count': int(
                        video['statistics'].get('commentCount', 0)
                    ),
                    'url': f"https://www.youtube.com/watch?v={video['id']}"
                }
                processed_videos.append(processed_video)
            except KeyError as e:
                print(f"Error Processing Video: {e}")
                continue
        
        return processed_videos

# TEST
if __name__ == "__main__":
    youtube_api = YouTubeAPI()

    # Test Search Videos
    print("Testing YouTube API Search...")
    videos = youtube_api.search_specific_videos(
        "Python", "data structures", "beginner"
    )
    print(f"Found {len(videos)} videos")

    # Print First 3 videos
    for i, video in enumerate(videos[:3], 1):
        print(f"\nVideo {i}:")
        print(f"Title: {video['title']}")
        print(f"Channel: {video['channel_title']}")
        print(f"Views: {video['view_count']}")
        print(f"URL: {video['url']}")
