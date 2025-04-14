from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
import requests
import logging

app = Flask(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Twilio credentials
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number
USER_STATE = {}  # To track user interactions

# Google Cloud credentials
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("PROCESSOR_LOCATION")
PROCESSOR_ID = os.getenv("PROCESSOR_ID")  # Use processor ID instead of name
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\KULUS_JP\AppData\Roaming\gcloud\application_default_credentials.json"

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def extract_year_of_publish(document):
    """Extract the year of publish from the document."""
    for entity in document.entities:
        if entity.type_ == "year_of_publish1":
            return entity.mention_text
    return "Year of publish not found."

def process_image(image_url):
    """Send the image to Google Cloud OCR and return extracted text."""
    try:
        opts = ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")
        client = documentai.DocumentProcessorServiceClient(client_options=opts)
        
        # Twilio credentials
        TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
        TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
        
        response = requests.get(image_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
        if response.status_code != 200:
            logging.error(f"Failed to fetch image from URL: {image_url}, status code: {response.status_code}")
            return "Failed to fetch image."

        image_content = response.content
        mime_type = response.headers.get('Content-Type')
        
        if not mime_type or not mime_type.startswith('image/'):
            logging.error(f"Invalid MIME type: {mime_type}")
            return "Invalid image format."

        logging.debug(f"Image content length: {len(image_content)}")
        logging.debug(f"MIME type: {mime_type}")

        raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
        
        processor_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"
        
        request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
        
        result = client.process_document(request=request)
        
        logging.debug(f"Document text: {result.document.text}")
        
        year_of_publish = extract_year_of_publish(result.document)
        return year_of_publish
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return "Error processing image."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    """Handles incoming WhatsApp messages."""
    incoming_msg = request.values.get("Body", "").strip().lower()
    sender = request.values.get("From")
    media_url = request.values.get("MediaUrl0")

    response = MessagingResponse()
    msg = response.message()
    
    if sender not in USER_STATE:
        USER_STATE[sender] = "idle"

    if incoming_msg == "cancel":
        USER_STATE[sender] = "idle"
        msg.body("Processing cancelled. Send a new image anytime.")
        return str(response)
    
    if USER_STATE[sender] == "waiting_for_image":
        if media_url:
            msg.body("Processing your image... Please wait.")
            USER_STATE[sender] = "processing"
            year_of_publish = process_image(media_url)
            msg.body(f"Extracted Year of Publish: {year_of_publish}")
            USER_STATE[sender] = "idle"
        else:
            msg.body("Please send an image.")
    
    elif USER_STATE[sender] == "idle":
        msg.body("Send me a photo for text extraction. Type 'cancel' to stop at any time.")
        USER_STATE[sender] = "waiting_for_image"

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
