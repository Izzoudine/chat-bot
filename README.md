# Mojaloop Load Tester Chatbot Backend

Backend server for the Mojaloop Load Tester Chatbot.

## Features

- **AI Chat**: Powered by Google Gemini 2.5 Flash (Streaming support).
- **Audio Analysis**: Upload audio files for AI analysis.
- **Load Testing**: Proxy CSV files to the load test engine.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python app.py
   ```
   The server runs on port **5001**.

## API Endpoints

### `POST /chat`
Send a message or audio file to the chatbot.
- **Form Data**:
    - `message`: (Text) The user's question.
    - `file`: (File) Optional audio file (.mp3, .wav, etc.).
- **Response**: Streaming text.

### `POST /upload-csv`
Upload a CSV file for load testing.
- **Form Data**:
    - `file`: (File) The CSV file.
- **Response**: A ZIP file containing the test report.

## Testing

Run the included test script to verify all endpoints:
```bash
python test_server.py
```
