# Environment Variables
load_dotenv()

app = Flask(__name__)
agent = VideoAgent()

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
  user_input = resquest.form.get('user_input')
  if not user_input:
    return jsonify({"error": "NO INPUT PROVIDED"}), 400
  
  response = agent.process_user_request(user_input)

  return jsonify({
    "response": response,
    "query": user_input
  })

if __name__ == '__main__':
  app.run(debug=True)