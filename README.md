# WhatsApp OCR GCP

This project connects WhatsApp with Google Cloud's custom Optical Character Recognition (OCR) service. Users can send images via WhatsApp, and the application will return the extracted text from the images.

## Features

- Send images through WhatsApp.
- Extract text from images using Google Cloud's Document AI (customized for these documents).
- Return the extracted text to the user via WhatsApp.

## Prerequisites

- Python 3.x
- Flask
- Twilio account
- Google Cloud account with Document AI enabled

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/whatsapp-ocr-gcp.git
   cd whatsapp-ocr-gcp
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory of the project with the following content:
   ```plaintext
   PROJECT_ID=your_google_cloud_project_id
   PROCESSOR_LOCATION=your_processor_location
   PROCESSOR_ID=your_processor_id
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   ```

5. Set up Google Cloud credentials:
   Make sure to set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your Google Cloud service account key JSON file.

## Usage

1. Run the application:
   ```bash
   python whatsapp_ocr_gcp.py
   ```

2. To expose your local server to the internet, use ngrok:
   ```bash
   ngrok http 5000
   ```
   This will provide you with a public URL that you can use to send WhatsApp messages to your bot.

3. Send a WhatsApp message to your Twilio number with an image to extract text.

4. The bot will respond with the extracted text from the image.

## Important Note

This application must be run with a service like ngrok when running locally, as Twilio requires a publicly accessible URL to send messages to your application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Twilio](https://www.twilio.com/) for the WhatsApp API.
- [Google Cloud Document AI](https://cloud.google.com/document-ai) for OCR capabilities.
