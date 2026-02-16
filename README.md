# ScribeMD - Transcript Parser

An AI-powered web application for analyzing medical clinic phone call transcripts. Uses advanced language models to automatically detect caller intent, extract structured information, and flag urgency levels.

## Features

- **AI-Powered Intent Detection**: Automatically identifies the reason for the call (appointment booking, prescription refill, urgent issue, etc.)
- **Structured Data Extraction**: Extracts caller information including name, date of birth, phone number
- **Urgency Flagging**: Automatically flags urgent medical issues
- **Confidence Scoring**: Provides confidence level for each analysis
- **Raw Transcript Input**: Paste phone call transcripts into the left panel
- **Parsed Data Output**: View the analyzed JSON data in the right panel with all extracted information
- **Submit Button**: Send transcript to server for AI analysis
- **Clear Button**: Reset both text fields

## Supported Intents

The system can detect these common medical clinic call types:
- appointment_booking
- appointment_cancellation
- appointment_reschedule
- prescription_refill
- lab_results
- billing_question
- insurance_question
- medication_side_effects
- **urgent_medical_issue** (flags high urgency)
- general_inquiry
- referral_request
- follow_up_call
- test_scheduling
- record_request
- other

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
- OpenAI API key (Claude 3.5 Sonnet or GPT-4 recommended)

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

4. **Configure API Key**
   - Open `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   - Get your API key from: https://platform.openai.com/api-keys

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   - Navigate to `http://localhost:5001`

## Usage

1. Enter or paste a medical clinic phone call transcript in the "Raw Transcript" field
2. Click the "Submit" button
3. The AI will analyze the transcript and display:
   - Detected intent (what the caller wants)
   - Extracted name, date of birth, phone number
   - Summary of the call reason
   - Urgency level (low, medium, high, critical)
   - Confidence score
   - Additional details (symptoms, medications, appointment dates, etc.)
4. Use the "Clear" button to reset both fields

### Example Input:
```
Hi, this is Sarah Cohen, born 03/12/1988. I need to book an appointment because 
I've had chest pain for two days. Please call me back at 310-555-2211.
```

### Example Output:
```json
{
  "intent": "urgent_medical_issue",
  "name": "Sarah Cohen",
  "dob": "1988-03-12",
  "phone": "310-555-2211",
  "summary": "Chest pain for two days - requires urgent appointment",
  "urgency": "high",
  "confidence": 0.95,
  "extracted_details": {
    "symptoms": ["chest pain"],
    "medications_mentioned": [],
    "appointment_dates": [],
    "other_info": ["Duration: 2 days"]
  },
  "raw_transcript": "Hi, this is Sarah Cohen..."
}
```

## API Endpoints

### POST `/api/parse`
Sends a phone call transcript to the server for AI analysis.

**Request:**
```json
{
  "transcript": "Hi, this is John Smith. I need to refill my prescription..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "intent": "prescription_refill",
    "name": "John Smith",
    "dob": "1975-05-15",
    "phone": "555-0123",
    "summary": "Caller requesting prescription refill",
    "urgency": "low",
    "confidence": 0.92,
    "extracted_details": {
      "symptoms": [],
      "medications_mentioned": [],
      "appointment_dates": [],
      "other_info": []
    },
    "raw_transcript": "Hi, this is John Smith..."
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Description of what went wrong"
}
```

## Adding Parsing Rules

Currently, the server returns the raw transcript as-is. To add parsing logic:

1. Edit `app.py` in the `parse_transcript()` function
2. Add your parsing rules and create new fields in the `parsed_data` dictionary
3. The changes will be reflected automatically (Flask debug mode enabled)


### Adding Custom Intents

To add new intents, edit the `CLINIC_INTENTS` list in `app.py`:

```python
CLINIC_INTENTS = [
    "appointment_booking",
    "your_new_intent_here",  # Add your custom intent
    # ... rest of intents
]
```

The AI will automatically learn to detect the new intent based on the name and context.

## Future Enhancements

- [ ] Integration with CRM
- [ ] Interactive: fix intent correction, setting appointments, etc.
- [ ] Custom intent configuration per clinic
- [ ] Call recording analysis
- [ ] Historical data analytics
- [ ] Integration with clinic management systems
- [ ] Real-time call monitoring
- [ ] Parallelism: Batch processing for multiple transcripts
- [ ] Export to CSV/PDF reports integration with database storage
- [ ] User authentication and Saas support
- [ ] Multi-language support


