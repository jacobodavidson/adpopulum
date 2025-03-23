from flask import Flask, request, render_template, jsonify
from improved_agent import ImprovedAgent
from dotenv import load_dotenv
import os
import traceback

# Load environment variables
load_dotenv()

app = Flask(__name__)
agent = ImprovedAgent()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_input = request.form.get('user_input')
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        
        print(f"Processing request: '{user_input}'")
        response = agent.process_user_request(user_input)
        print("Request completed")
        
        return jsonify({
            "response": response,
            "query": user_input
        })
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Error processing request: {str(e)}")
        print(error_traceback)
        return jsonify({
            "error": "An error occurred while processing your request",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    # Enable threading to prevent blocking
    app.run(debug=True, threaded=True)