# ad Populum - AI YouTube Learning Video Recommender

An AI-powered agent that finds the best YouTube educational videos based on your learning needs. Simply enter a topic and your learning level, and ad Populum will intelligently rank and recommend the most relevant educational videos.

## Features

- **Natural Language Understanding**: Enter queries in natural language and the AI extracts your topic and learning level
- **Intelligent Video Ranking**: Videos are ranked based on relevance, quality, engagement, and appropriateness for your learning level
- **Clean User Interface**: Simple chat interface with visual video recommendations
- **YouTube Integration**: Seamlessly searches YouTube's vast library of educational content
- **Conversational Experience**: Chat-like interface for a more natural interaction

## Installation

### Prerequisites

- Python 3.8+
- A Google API key with YouTube Data API v3 enabled

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/jacobodavidson/ad-populum.git
   cd ad-populum
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   
   Create a `.env` file in the project root:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## How It Works

1. **Natural Language Processing**: When you enter a query, the AI agent extracts:
   - The subject you want to learn about
   - Your preferred learning level (beginner, intermediate, advanced)

2. **YouTube Search**: The agent constructs an optimized search query and calls the YouTube API

3. **Intelligent Ranking**: Videos are scored and ranked based on:
   - Relevance to your topic
   - Content quality (views, likes, engagement)
   - Appropriateness for your learning level
   - Educational content indicators

4. **Visual Presentation**: Results are displayed in an easy-to-browse format with thumbnails and essential information

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: YouTube Data API v3
- **AI Components**: Natural Language Processing, Custom Ranking Algorithm

## Future Enhancements

- User accounts for saving favorite videos and tracking learning progress
- Advanced filtering options (video length, publication date, etc.)
- Related topic suggestions based on search history
- Feedback mechanism to improve recommendations
- Mobile app version

## Project Structure
adpopulum/
├── templates/
│   └── index.html         # Frontend HTML template
├── static/
│   └── style.css          # Optional CSS for styling
├── agent.py               # Core logic for video search and ranking
├── youtube_api.py         # YouTube API integration
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- YouTube Data API for providing access to the video data
- Flask for the web framework
- Google API Client Library for Python

## Contact

For questions or feedback, feel free to reach out:

Email: jacobodavidson@outlook.com
GitHub: jacobodavidson

---
