from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client with API key from .env
client = None
api_key = os.getenv('OPENAI_API_KEY')

if api_key:
    try:
        print(f"✅ Initializing OpenAI client with API key...")
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client created successfully")
    except Exception as e:
        print(f"❌ Error creating OpenAI client: {e}")
        client = None
else:
    print("❌ No OPENAI_API_KEY found in .env file")

# Available intents for a medical clinic
CLINIC_INTENTS = [
    "appointment_booking",
    "appointment_cancellation",
    "appointment_reschedule",
    "prescription_refill",
    "lab_results",
    "billing_question",
    "insurance_question",
    "medication_side_effects",
    "urgent_medical_issue",
    "general_inquiry",
    "referral_request",
    "follow_up_call",
    "test_scheduling",
    "record_request",
    "other"
]

URGENCY_LEVELS = ["low", "medium", "high", "critical"]

def detect_intent_and_extract_data(transcript):
    """
    Uses OpenAI API to detect intent and extract structured information from transcript.
    Returns parsed JSON with intent, extracted data, and urgency flag.
    """
    try:
        system_prompt = f"""You are an AI assistant for a medical clinic phone call analysis system.
        
Your task is to analyze phone transcripts and:
1. Detect the caller's intent
2. Extract structured information
3. Flag urgency level

Available intents: {', '.join(CLINIC_INTENTS)}
Urgency levels: {', '.join(URGENCY_LEVELS)}

Return ONLY valid JSON (no markdown, no extra text) with this exact structure:
{{
    "intent": "one of the intents",
    "name": "caller's full name or null",
    "dob": "date of birth in YYYY-MM-DD format or null",
    "phone": "callback phone number or null",
    "summary": "brief summary of reason for call",
    "urgency": "urgency level",
    "confidence": 0.0-1.0,
    "extracted_details": {{
        "symptoms": [],
        "medications_mentioned": [],
        "appointment_dates": [],
        "other_info": []
    }}
}}"""

        message = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=1024,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"Analyze this clinic phone transcript:\n\n{transcript}"
                }
            ]
        )

        # Parse the response
        response_text = message.choices[0].message.content.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        response_text = response_text.strip()

        parsed_data = json.loads(response_text)

        return {
            "success": True,
            "data": parsed_data
        }

    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Failed to parse AI response: {str(e)}",
            "raw_response": response_text if 'response_text' in locals() else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"API Error: {str(e)}"
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/parse', methods=['POST'])
def parse_transcript():
    """
    Receives raw transcript from frontend and returns parsed JSON data
    using AI to detect intent and extract structured information.
    """
    data = request.get_json()
    raw_transcript = data.get('transcript', '').strip()

    if not raw_transcript:
        return jsonify({
            "success": False,
            "error": "Transcript cannot be empty"
        }), 400

    if not client:
        return jsonify({
            "success": False,
            "error": "API not configured. Please: 1) Run 'pip install -r requirements.txt', 2) Add your API key to .env file"
        }), 500

    # Use AI to detect intent and extract data
    result = detect_intent_and_extract_data(raw_transcript)

    if not result["success"]:
        return jsonify(result), 500

    # Add raw transcript to the response
    parsed_data = result["data"]
    parsed_data["raw_transcript"] = raw_transcript

    return jsonify({
        "success": True,
        "data": parsed_data
    })

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5002)

