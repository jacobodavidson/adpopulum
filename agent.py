import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from dotenv import load_dotenv

# Environment Variables
load_dotenv()

# Download NLTK Resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

class VideoAgent:
    def __init__(self):
        """Initialize the VideoAgent class."""
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

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

    def process_user_request(self, user_input):
        # Main Method to Process User Input
        """ONLY RETURNS EXTRACTED PARAMETERS - FIX LATER"""
        query_params = self.process_query(user_input)
        return (f"Extracted parameters: Subject: {query_params['subject']}, "
                f"Subtopic: {query_params['subtopic']}, "
                f"Level: {query_params['level']}")
    
    # TEST
    if __name__ == "__main__":
        agent = VideoAgent()

        # Test with Sample User Inputs
        test_queries = [
            "I want to learn Python programming for beginners",
            "How to create a website using HTML and CSS",
            "Advanced machine learning tutorials",
            "Learn data science for beginners",
            "How to build a mobile app for Android",
            "Intermediate level Java programming",
            "Python tutorials for experienced developers",
            "Introduction to web development",
            "Advanced Python projects for professionals"
        ]

        for query in test_queries:
            print(f"Query: {query}")
            print(agent.process_user_request(query))
            print()