from flask import Flask, request, render_template, jsonify
from agent import VideoAgent
from dotenv import load_dotenv
import os
import traceback

# Load Environment Variables
load_dotenv()

app = Flask(__name__)

# Initialize the agent
try:
  agent = VideoAgent()
  print("Agent initialized successfully")
except Exception as e:
  print(f"Error initializing agent: {e}")
  print(traceback.format_exc())
  exit(1)

@app.route('/')
def home():
  # Render Home Page
  return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
  """Process user request and return response"""
  try:
    # Get user input
    user_input = request.form.get('user_input')
    if not user_input or user_input.strip() == '':
      return jsonify({
        "error": "Please enter a topic and learning level"
      }), 400
    
    # Process request
    print(f"Processing request: '{user_input}'")
    response = agent.process_user_request(user_input)
    print("Request processed successfully")
    
    return jsonify({
      "response": response,
      "query": user_input
    })
  except Exception as e:
    # Log the error
    error_traceback = traceback.format_exc()
    print(f"Error processing request: {str(e)}")
    print(error_traceback)
    
    # Return error response
    return jsonify({
      "error": "An error occurred while processing your request",
      "details": str(e)
    }), 500

if __name__ == '__main__':
  # Get port from environment variable or use default
  port = int(os.environ.get('PORT', 5000))
  
  # Run the app
  app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
