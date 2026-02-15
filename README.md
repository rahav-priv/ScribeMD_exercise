# ScribeMD - Transcript Parser

A simple web application for parsing and processing transcripts. Built with Flask and vanilla JavaScript.

## Features

- **Raw Transcript Input**: Paste your raw transcript text into the left panel
- **Parsed Data Output**: View the parsed JSON data in the right panel
- **Submit Button**: Send transcript to server for processing
- **Clear Button**: Reset both text fields
- **Real-time Feedback**: Status messages for user actions

## Project Structure

```
scribemd/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Frontend HTML
└── static/
    ├── style.css         # Styling
    └── script.js         # Frontend logic
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd scribemd
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:5001`

## Usage

1. Enter or paste your transcript in the "Raw Transcript" field
2. Click the "Submit" button
3. The server will process it and display the parsed JSON in the "Parsed Data" field
4. Use the "Clear" button to reset both fields

## API Endpoints

### POST `/api/parse`
Sends raw transcript to the server for parsing.

**Request:**
```json
{
  "transcript": "Your raw transcript text here..."
}
```

**Response:**
```json
{
  "raw_transcript": "Your raw transcript text here..."
}
```

## Adding Parsing Rules

Currently, the server returns the raw transcript as-is. To add parsing logic:

1. Edit `app.py` in the `parse_transcript()` function
2. Add your parsing rules and create new fields in the `parsed_data` dictionary
3. The changes will be reflected automatically (Flask debug mode enabled)

## Development

The app runs with Flask's debug mode enabled on **http://localhost:5001**, so changes to Python files will automatically reload the server. Static files (CSS, JS) are served from the `static/` directory.

## Future Enhancements

- [ ] Advanced parsing rules
- [ ] Multiple input formats (audio, video, etc.)
- [ ] Export functionality (PDF, DOCX)
- [ ] User authentication
- [ ] Cloud storage integration

## License

MIT License - feel free to use this for personal or commercial projects.

