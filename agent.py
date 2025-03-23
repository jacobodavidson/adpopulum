import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
import math
from datetime import datetime
import traceback
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

class VideoAgent:
  def __init__(self):
    # Initialize YouTube API client
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
      raise ValueError(
        "YouTube API key not found. Please set YOUTUBE_API_KEY in .env file."
      )
    
    self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Define learning levels and their synonyms
    self.learning_levels = {
      'beginner': [
        'beginner', 'basic', 'intro', 'introduction', 'starting', 'novice',
        'fundamentals', 'newbie', 'elementary', 'starter', 'new', 'start',
        'noob'
      ],
      'intermediate': [
        'intermediate', 'middle', 'mid-level', 'improving', 'advancing',
        'moderate', 'medium', 'average', 'mid', 'in-between', 'progressing',
        'developing'
      ],
      'advanced': [
        'advanced', 'expert', 'professional', 'mastery', 'proficient',
        'master', 'pro', 'skilled', 'experienced', 'senior', 'hard'
      ]
    }
    
    # Common words to ignore in subject extraction
    self.common_words = [
      'find', 'search', 'get', 'show', 'me', 'about', 'on', 'for', 'videos',
      'video', 'tutorials', 'tutorial', 'lessons', 'lesson', 'please', 'want',
      'need', 'looking', 'help', 'with', 'learning', 'learn', 'study', 'a',
      'an', 'the', 'how', 'to', 'in', 'at', 'from', 'by', 'using', 'course',
      'courses', 'class', 'classes', 'training', 'guide', 'guides'
    ]
  
  def extract_parameters(self, user_input):
    # Extract Learning Level, Subject
    user_input = user_input.lower()
    
    # Extract learning level
    level = 'beginner'  # Default
    level_found = False
    level_match = ""
    
    for lvl, keywords in self.learning_levels.items():
      for keyword in keywords:
        if (
          f" {keyword} " in f" {user_input} " or
          user_input.startswith(f"{keyword} ") or
          user_input.endswith(f" {keyword}")
        ):
          level = lvl
          level_found = True
          level_match = keyword
          break
      if level_found:
        break
    
    # Remove the level keyword before extracting subject
    if level_match:
      user_input = re.sub(
        r'\b' + re.escape(level_match) + r'\b', '', user_input
      )
    
    # Clean up the input
    user_input = re.sub(r'[^\w\s]', '', user_input).strip()
    
    # Split the remaining input into words
    words = user_input.split()
    
    # Filter out common words
    filtered_words = [
      w for w in words if w.lower() not in self.common_words
    ]
    
    if not filtered_words:
      # Use original words if filtering removed everything
      subject = ' '.join(words) if words else "programming"
    else:
      # Use all remaining words as the subject
      subject = ' '.join(filtered_words)
    
    return {
      'subject': subject,
      'level': level
    }
  
  def search_videos(self, params, max_results=100):
    # Search YouTube for Matching Videos
    try:
      subject = params['subject']
      level = params['level']
      
      # Create search query
      search_query = f"{subject} {level} tutorial"
      print(f"Searching YouTube for: '{search_query}'")
      
      video_ids = []
      next_page_token = None
      results_fetched = 0

      while results_fetched < max_results:
        # Fetch a batch of results
        search_response = self.youtube.search().list(
          q=search_query,
          part='id',
          maxResults=min(50, max_results - results_fetched),
          type='video',
          relevanceLanguage='en',
          pageToken=next_page_token
        ).execute()

        # Extract video IDs from the response
        video_ids.extend([
          item['id']['videoId']
          for item in search_response.get('items', [])
        ])

        # Update the number of results fetched
        results_fetched += len(search_response.get('items', []))

        # Check if there is another page of results
        next_page_token = search_response.get('nextPageToken')
        if not next_page_token:
          break

      print(f"Total video IDs retrieved: {len(video_ids)}")
      return video_ids
    except HttpError as e:
      print(f"YouTube API error: {e}")
      return []
    except Exception as e:
      print(f"Error searching videos: {e}")
      print(traceback.format_exc())
      return []
  
  def search_videos(self, params):
    # Search YouTube for videos matching subject and level
    try:
      subject = params['subject']
      level = params['level']
      
      # Create search query
      search_query = f"{subject} {level} tutorial"
      print(f"Searching YouTube for: '{search_query}'")
      
      # Perform search
      search_response = self.youtube.search().list(
        q=search_query,
        part='id,snippet',
        maxResults=20,
        type='video',
        relevanceLanguage='en'
      ).execute()
      
      # Extract video IDs
      video_ids = [
        item['id']['videoId']
        for item in search_response.get('items', [])
      ]
      
      if not video_ids:
        return []
      
      # Get more details about videos
      videos_response = self.youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=','.join(video_ids)
      ).execute()
      
      # Process videos
      processed_videos = []
      
      for video in videos_response.get('items', []):
        try:
          # Extract statistics with defaults for missing values
          stats = video.get('statistics', {})
          view_count = int(stats.get('viewCount', 0))
          like_count = int(stats.get('likeCount', 0))
          comment_count = int(stats.get('commentCount', 0))
          
          # Calculate engagement score
          engagement = 0
          if view_count > 0:
            engagement = (like_count + comment_count) / view_count
          
          # Calculate freshness score
          published_at = datetime.strptime(
            video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'
          )
          current_time = datetime.utcnow()
          days_since_publication = (current_time - published_at).days
          
          freshness = 1.0
          if days_since_publication <= 365: # 1 year
            freshness = 1.0
          elif days_since_publication <= 730: # 2 years
            freshness = 0.9
          elif days_since_publication <= 1095: # 3 years
            freshness = 0.8
          elif days_since_publication > 1095: # 4 years
            freshness = 0.7

          # Create video object
          processed_video = {
            'id': video['id'],
            'title': video['snippet']['title'],
            'description': video['snippet']['description'],
            'channel': video['snippet']['channelTitle'],
            'published_at': video['snippet']['publishedAt'],
            'thumbnail': (
              video['snippet']['thumbnails'].get('high', {}).get('url', '') or
              video['snippet']['thumbnails'].get('medium', {}).get('url', '') or
              video['snippet']['thumbnails'].get('default', {}).get('url', '')
            ),
            'view_count': view_count,
            'like_count': like_count,
            'comment_count': comment_count,
            'engagement': engagement,
            'freshness': freshness,
            'url': f"https://www.youtube.com/watch?v={video['id']}"
          }
          
          # Calculate relevance score for ranking
          processed_video['score'] = self.calculate_video_score(
            processed_video, subject, level
          )
          processed_videos.append(processed_video)
          
        except KeyError as e:
          print(f"Missing data in video {video.get('id', 'unknown')}: {e}")
          continue
      
      # Sort by score (highest first)
      processed_videos.sort(key=lambda x: x['score'], reverse=True)
      
      # Return top 5 videos
      return processed_videos[:5]
      
    except HttpError as e:
      print(f"YOUTUBE API ERROR: {e}")
      return []
    except Exception as e:
      print(f"ERROR SEARCHING VIDEOS: {e}")
      print(traceback.format_exc())
      return []
  
  def calculate_video_score(self, video, subject, level):
    # Calculate a relevance score for the video
    score = 0
    
    # Base score from views (logarithmic scale)
    if video['view_count'] > 0:
      score += min(math.log(video['view_count'], 2), 10) * 75  # Cap log value
    else:
      score += 0
    
    # Like count contribution
    if video['like_count'] > 0:
      score += min(math.log(video['like_count'], 2), 10) * 50
    else:
      score += 0
    
    # Engagement factor
    score += video['engagement'] * 1000
    
    # Freshness factor
    score += video['freshness'] * 1000

    # MIGHT NOT EVEN NEED THESE BELOW BECAUSE IT IS ALREADY IN THE SEARCH QUERY   
    # Title relevance
    title_lower = video['title'].lower()
    subject_keywords = subject.lower().split()

    # Count matching keywords in title
    keyword_matches = sum(
      1 for keyword in subject_keywords if keyword in title_lower
    )
    if keyword_matches > 0:
      score += keyword_matches * 100
    
    # Check for exact phrase match
    if subject.lower() in title_lower:
      score += 500
    
    # Check for learning level indicators
    level_terms = self.learning_levels[level]
    if any(term in title_lower for term in level_terms):
      score += 500
    
    # Educational content indicators
    educational_terms = [
      'tutorial', 'learn', 'course', 'lesson', 'how to', 'explained', 'guide'
    ]
    if any(term in title_lower for term in educational_terms):
      score += 500
    
    return score
  
  def format_response(self, videos, params):
    # Format Response as Natural Language
    if not videos:
      return (
        f"I couldn't find any good videos about {params['subject']} for "
        f"{params['level']} level learners. Could you try a different search "
        f"query or learning level?"
      )
    
    # Create response message
    response = (
      f"Here are some {params['level']} level videos for "
      f"'{params['subject']}':\n\n"
    )
    
    # Add each video to the response
    for i, video in enumerate(videos, 1):
      response += f"{i}. {video['title']} by {video['channel']}\n"
      response += f"   {video['view_count']:,} views • {video['url']}\n\n"
    
    return response
  
  def process_user_request(self, user_input):
    """Main method to process a user request"""
    try:
      # Extract parameters from user input
      params = self.extract_parameters(user_input)
      print(f"Extracted parameters: {params}")
      
      # Find videos matching parameters
      videos = self.search_videos(params)
      
      # Format response
      response = self.format_response(videos, params)
      
      return response
    except Exception as e:
      print(f"ERROR PROCESSING REQUEST: {e}")
      print(traceback.format_exc())
      return (
        "ERROR PROCESSING REQUEST."
        "PLEASE TRY AGAIN."
      )
