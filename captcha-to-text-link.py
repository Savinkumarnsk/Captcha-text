from flask import Flask, request, jsonify
from PIL import Image
import requests
import os
import io
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key="use your gemini API KEY Here")
model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

@app.route('/image-to-text', methods=['POST'])
def image_to_text():
    try:
        # Accept JSON input with "captcha_url"
        data = request.get_json()
        captcha_url = data.get('captcha_url')

        if not captcha_url:
            return jsonify({'error': 'Missing captcha_url in request'}), 400

        # Download the image from URL
        response = requests.get(captcha_url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to download image from URL'}), 400

        # Convert image to PIL Image
        image_bytes = io.BytesIO(response.content)
        img = Image.open(image_bytes).convert("RGB")

        # Gemini Prompt
        prompt = "Extract all visible text from this image. Don't explain anything—just return the plain text."

        # Generate content with Gemini
        result = model.generate_content([img, prompt])
        extracted_text = result.text.strip()

        return jsonify({'text': extracted_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
