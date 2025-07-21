Image-to-Text Flask Application
This is a simple Flask application that provides an API endpoint to extract text from an image URL using the Google Gemini AI model.

Features
Accepts an image URL via a POST request.

Downloads the image from the provided URL.

Uses the Gemini 2.5 Flash model to perform Optical Character Recognition (OCR) and extract text.

Returns the extracted text in a JSON response.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8+

pip (Python package installer)

Installation
Clone the repository (if applicable) or save your Flask application code (e.g., app.py).

Create a virtual environment (recommended):

python -m venv venv

Activate the virtual environment:

On Windows:

.\venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

Install the required dependencies:
The necessary libraries are listed in your requirements.txt Canvas.

pip install -r requirements.txt

Configuration
Google Gemini API Key:
You need a Google Gemini API key. Replace "AIzaSyBh-gQTCd4NrtSeO534KM8FznaMdDwXI94" in your app.py file with your actual API key.

genai.configure(api_key="YOUR_GEMINI_API_KEY")

Note: For production environments, it's highly recommended to use environment variables to store your API key instead of hardcoding it.

Usage
Run the Flask application:

python app.py

The application will start on http://127.0.0.1:5000/ by default.

Make a POST request to the /image-to-text endpoint:
Send a JSON payload containing the captcha_url of the image you want to process.

Example using curl:

curl -X POST -H "Content-Type: application/json" \
     -d '{"captcha_url": "https://example.com/path/to/your/image.png"}' \
     http://127.0.0.1:5000/image-to-text

Replace https://example.com/path/to/your/image.png with the actual URL of the image.

Example successful response:

{
  "text": "Extracted text from image"
}

Example error response:

{
  "error": "Missing captcha_url in request"
}

Process Flow
The image-to-text endpoint handles the following steps:

Receive Request: The Flask application receives a POST request to the /image-to-text endpoint. It expects a JSON body with a key named captcha_url.

Validate Input: It checks if the captcha_url is present in the request payload. If not, it returns a 400 Bad Request error.

Download Image: It uses the requests library to download the image from the provided captcha_url. If the download fails (e.g., due to a bad URL or network issue), it returns a 400 error.

Prepare Image for Gemini: The downloaded image content (bytes) is converted into a PIL.Image.Image object, which is the format expected by the Gemini API for image input.

Call Gemini API:

A specific prompt ("Extract all visible text from this image. Don't explain anything—just return the plain text.") is prepared to guide the Gemini model.

The model.generate_content([img, prompt]) call sends both the image and the prompt to the configured Gemini model (gemini-2.5-flash).

Extract and Return Text:

The response from the Gemini model (result) contains the generated text.

The result.text.strip() extracts the plain text and removes any leading/trailing whitespace.

Finally, the extracted text is returned as a JSON response with the key text.

Error Handling: A try-except block catches any general exceptions during the process and returns a 500 Internal Server Error with the error message.
