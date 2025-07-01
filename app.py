from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv # Import load_dotenv


load_dotenv()

app = Flask(__name__)


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set it in your .env file or your deployment environment.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def index():
    """
    Renders the main index page of the application.
    """
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    """
    Handles translation requests.
    Expects a JSON payload with 'text' and 'language'.
    """
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', '')

    if not text:
        return jsonify({'result': 'Error: No text provided for translation.'}), 400
    if not language:
        return jsonify({'result': 'Error: No target language provided.'}), 400

    prompt = f"Translate the following text to {language}:\n{text}"
    try:
        response = model.generate_content(prompt)
        # Check if the response contains actual text
        if response and response.text:
            return jsonify({'result': response.text.strip()})
        else:
            return jsonify({'result': 'Error: Translation service returned an empty response.'}), 500
    except Exception as e:
        # Log the error for debugging purposes (optional, but recommended in production)
        print(f"Error during translation: {e}")
        return jsonify({'result': f'Error: Could not process translation. {str(e)}'}), 500

if __name__ == '__main__':
    # When running locally, debug=True is useful.
    # In production, set debug=False and use a production-ready WSGI server (e.g., Gunicorn).
    app.run(debug=True)