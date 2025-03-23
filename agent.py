import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
import math
from datetime import datetime
import traceback
from dotenv import load_dotenv

# Environment Variables
load_dotenv()

class VideoAgent:
    def __init__(self):
        # Initialize YouTube API Client
        api_key = os.getenv('YOUTUBE_API_KEY')
        if not api_key:
            raise ValueError('YOUTUBE_API_KEY is not set')
        
        self.youtube = build('youtube', 'v3', developerKey=api_key)

        # Define Learning Levels
        self.learning_levels = {
            'beginner': ['beginner', 'basic', 'easy', 'introductory', 'intro',
                         'new', 'novice', 'simple', 'starter', 'fundamental',
                         'elementary', 'foundational', 'primary', 'rudimentary',
                         'underlying', 'entry-level', 'first-time', 'learner',
                         'starting'],
            'intermediate': ['intermediate', 'mid-level', 'mid', 'average',
                             'moderate', 'medium', 'standard', 'interim',
                             'in-between', 'center', 'transitional',
                             'progressive', 'developing', 'competent',
                             'practiced', 'skilled'],
            'advanced': ['advanced', 'complex', 'difficult', 'challenging',
                         'complicated', 'sophisticated', 'intricate',
                         'high-level', 'expert', 'master', 'pro',
                         'professional', 'specialist', 'specialized', 'elite',
                         'experienced', 'veteran', 'seasoned', 'high-skill',
                         'top-tier']
        }

        # Common words to ignore in subject extraction
        self.common_words = ['find', 'search', 'get', 'show', 'me', 'about', 'on', 'for', 'videos', 
                             'video', 'tutorials', 'tutorial', 'lessons', 'lesson', 'please', 
                             'want', 'need', 'looking', 'help', 'with', 'learning', 'learn', 'study', 
                             'course', 'courses', 'class', 'classes', 'training', 'guide', 'guides']

    def process_query(self, user_input):
        # Extract Subject, Subtopic, and Learning Level from Input
        # Tokenize and Preprocess User Input
        tokens = word_tokenize(user_input.lower())
        filtered_tokens = [self.lemmatizer.lemmatize(w) for w in tokens
                           if w not in self.stop_words]

        # Extract Learning Level
        level = self._extract_learning_level(filtered_tokens,
                                             user_input.lower())

        # Extract Subject and Subtopic
        # Remove Learning Level Keywords from Tokens
        level_terms = []
        for terms in self.learning_levels.values():
            level_terms.extend(terms)

        content_tokens = [t for t in filtered_tokens if t not in level_terms]

        # Simplified Subject and Subtopic Extraction
        # First Significant Noun Phrase is Subject
        # Second Significant Noun Phrase is Subtopic (Try to improve this)

        if len(content_tokens) >= 3:
            subject = content_tokens[0]
            subtopic = ' '.join(content_tokens[1:3])
        elif len(content_tokens) == 2:
            subject = content_tokens[0]
            subtopic = content_tokens[1]
        else:
            subject = ' '.join(content_tokens)
            subtopic = ""

        return {
            'subject': subject,
            'subtopic': subtopic,
            'level': level
        }

    def _extract_learning_level(self, tokens, original_input):
        # Extract Learning Level from User Input with Keyword Matching
        for level, synonyms in self.learning_levels.items():
            if any(syn in tokens for syn in synonyms) or any(
                    syn in original_input for syn in synonyms):
                return level
        return 'beginner'  # Default Learning Level
    
    def recommend_videos(self, query_params):
        # Returns List of Videos Sorted by Relevance Score
        subject = query_params['subject']
        subtopic = query_params['subtopic']
        level = query_params['level']

        # Get Videos from YouTube API
        videos = self.youtube_api.search_specific_videos(
            subject, subtopic, level)
        
        if not videos:
            return []
        
        # Calculate Relevance Score for Each Video and Sort
        for video in videos:
            video['score'] = self.calculate_relevance_score(video, level, subject, subtopic)
        
        videos.sort(key=lambda x: x['score'], reverse=True)

        return videos[:5]
    
    def calculate_relevance_score(self, video, level, subject, subtopic):
        # Calculates Relevance Score for a Video
        score = 0

        # View Count Score
        if video['view_count'] > 0:
            score += math.log(video['view_count']) * 10
        
        # Like Count Score
        if video['like_count'] > 0:
            score += math.log(video['like_count']) * 5

        # Title Subject/Subtopic Match Score
        title_lower = video['title'].lower()
        if subject.lower() in title_lower:
            score += 30
        if subtopic.lower() in title_lower:
            score += 20
        
        # Check for Level Keywords in Title
        level_terms = self.learning_levels[level]
        if any(term in title_lower for term in level_terms):
            score += 25

        # Educational Content Score
        educational_terms = ['tutorial', 'course', 'lesson', 'learn',
                             'education', 'how to', 'guide', 'explained']
        if any(term in title_lower for term in educational_terms):
            score += 15
        
        return score
    
    def generate_response(self, videos, query_params):
        # Gerenate Response Message with Reccomendations
        if not videos:
            return f"I couldn't find any videos about {query_params['subject']} {query_params['subtopic']} for {query_params['level']} learners. Could you try a different topic or learning level?"
        
        response = f"Based on your interest in learning about {query_params['subject']} {query_params['subtopic']} at a {query_params['level']} level, here are my top recommendations:\n\n"
        
        for i, video in enumerate(videos, 1):
            response += f"{i}. \"{video['title']}\" by {video['channel_title']}\n"
            response += f"   {video['view_count']:,} views • {video['url']}\n\n"
            
        response += "These videos were selected based on relevance, popularity, and their match to your specified learning level."
        return response

    def process_user_request(self, user_input):
        # Main Method to Process User Input
        # Extract Subject, Subtopic, and Learning Level
        query_params = self.process_query(user_input)

        # Get Recommended Videos
        videos = self.recommend_videos(query_params)

        # Generate Response Message
        response = self.generate_response(videos, query_params)
      
    # TEST
    if __name__ == "__main__":
        agent = VideoAgent()

        test_query = "I want to learn Python data structures for beginners"
        print(f"Processing Query: {test_query}")
        print(agent.process_user_request(test_query))