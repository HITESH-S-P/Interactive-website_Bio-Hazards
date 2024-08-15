import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# Get the API key from environment variables
API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Generative AI with the API key
genai.configure(api_key=API_KEY)

# Initialize the model and chat with the specified instruction
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
instruction = "answer as if you are a bio-hazard scientist chatbot and give your answer in points wise and each point of 1 or 2 lines,clear and small and your name is R.V.C.E Bio-hazard Chatbot"

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    # Get the question from the request data
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400

    # Send the question to the AI model and get the response
    response = chat.send_message(question+instruction)
    
    # Remove asterisks from the response text
    cleaned_response = response.text.replace('*', '')

    return jsonify({"response": cleaned_response})

@app.route('/')
def index():
    # Render the HTML page
    return render_template('chatbot.html')

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True, port=5000)
