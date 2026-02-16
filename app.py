from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta

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

# Define intent-specific schemas
INTENT_SCHEMAS = {
    "appointment_booking": {
        "desired_appointment_date": {
            "type": ["string", "null"],
            "description": "Desired appointment date in YYYY-MM-DD format"
        },
        "appointment_type": {
            "type": ["string", "null"],
            "description": "Type of appointment (e.g., checkup, consultation, follow-up)"
        }
    },
    "appointment_cancellation": {
        "original_appointment_date": {
            "type": ["string", "null"],
            "description": "Original appointment date in YYYY-MM-DD format"
        },
        "cancellation_reason": {
            "type": ["string", "null"],
            "description": "Reason for cancellation"
        }
    },
    "appointment_reschedule": {
        "original_appointment_date": {
            "type": ["string", "null"],
            "description": "Original appointment date in YYYY-MM-DD format"
        },
        "desired_new_time": {
            "type": ["string", "null"],
            "description": "Desired new appointment date/time in YYYY-MM-DD format"
        }
    },
    "prescription_refill": {
        "medication_name": {
            "type": ["string", "null"],
            "description": "Name of medication to refill"
        },
        "refill_count": {
            "type": ["string", "null"],
            "description": "Number of refills needed"
        }
    },
    "lab_results": {
        "test_type": {
            "type": ["string", "null"],
            "description": "Type of test/lab result being inquired about"
        }
    },
    "billing_question": {
        "invoice_number": {
            "type": ["string", "null"],
            "description": "Invoice or billing reference number if mentioned"
        },
        "question_type": {
            "type": ["string", "null"],
            "description": "Type of billing question (payment plan, charges, insurance, etc.)"
        }
    },
    "insurance_question": {
        "insurance_provider": {
            "type": ["string", "null"],
            "description": "Insurance company name if mentioned"
        },
        "question_type": {
            "type": ["string", "null"],
            "description": "Type of insurance question (coverage, deductible, provider network, etc.)"
        }
    },
    "medication_side_effects": {
        "medication_name": {
            "type": ["string", "null"],
            "description": "Name of medication causing side effects"
        },
        "side_effects": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of side effects reported"
        }
    },
    "urgent_medical_issue": {
        "symptoms": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of symptoms or medical issues"
        },
        "duration": {
            "type": ["string", "null"],
            "description": "How long the issue has been occurring"
        }
    },
    "referral_request": {
        "specialist_type": {
            "type": ["string", "null"],
            "description": "Type of specialist needed (e.g., cardiologist, dermatologist)"
        }
    },
    "test_scheduling": {
        "test_type": {
            "type": ["string", "null"],
            "description": "Type of test to schedule (blood work, imaging, etc.)"
        },
        "preferred_date": {
            "type": ["string", "null"],
            "description": "Preferred test date in YYYY-MM-DD format"
        }
    }
}

def build_schema_for_intent(intent):
    """
    Build a dynamic schema based on the detected intent.
    Includes common fields plus intent-specific fields.
    """
    # Common fields for all intents
    properties = {
        "intent": {
            "type": "string",
            "enum": CLINIC_INTENTS,
            "description": "The caller's intent from the call"
        },
        "name": {
            "type": ["string", "null"],
            "description": "Caller's full name"
        },
        "dob": {
            "type": ["string", "null"],
            "description": "Date of birth in YYYY-MM-DD format"
        },
        "phone": {
            "type": ["string", "null"],
            "description": "Caller's callback phone number"
        },
        "summary": {
            "type": "string",
            "description": "Brief one-sentence summary of the call reason"
        },
        "urgency": {
            "type": "string",
            "enum": URGENCY_LEVELS,
            "description": "Urgency level of the call"
        },
        "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Confidence score (0-1)"
        }
    }

    # Add intent-specific fields if they exist
    if intent in INTENT_SCHEMAS:
        properties.update(INTENT_SCHEMAS[intent])

    # Build required fields list
    required_fields = ["intent", "name", "dob", "phone", "summary", "urgency", "confidence"]
    if intent in INTENT_SCHEMAS:
        required_fields.extend(INTENT_SCHEMAS[intent].keys())

    return {
        "type": "object",
        "properties": properties,
        "required": required_fields,
        "additionalProperties": False
    }

def get_intent_instructions(intent):
    """
    Provide intent-specific extraction instructions
    """
    instructions = {
        "appointment_booking": "- Extract desired_appointment_date: when they want to schedule\n- Extract appointment_type: what kind of appointment",
        "appointment_cancellation": "- Extract original_appointment_date: when their appointment was scheduled\n- Extract cancellation_reason: why they're canceling",
        "appointment_reschedule": "- Extract original_appointment_date: their current appointment date\n- Extract desired_new_time: the new date/time they want",
        "prescription_refill": "- Extract medication_name: what medication they need\n- Extract refill_count: how many refills they need",
        "lab_results": "- Extract test_type: what test results they're asking about",
        "billing_question": "- Extract invoice_number: any billing/invoice reference number\n- Extract question_type: what they want to know (charges, payment plan, insurance, etc.)",
        "insurance_question": "- Extract insurance_provider: their insurance company name\n- Extract question_type: what they want to know (coverage, deductible, network, etc.)",
        "medication_side_effects": "- Extract medication_name: what medication is causing issues\n- Extract side_effects: list of side effects they're experiencing",
        "urgent_medical_issue": "- Extract symptoms: list of symptoms or medical issues\n- Extract duration: how long they've had these symptoms",
        "referral_request": "- Extract specialist_type: what type of specialist they need",
        "test_scheduling": "- Extract test_type: what test they want to schedule\n- Extract preferred_date: when they'd like to schedule it",
    }
    return instructions.get(intent, "")

def detect_intent_and_extract_data(transcript):
    """
    Two-step process:
    1. First, detect the intent
    2. Then, build dynamic schema based on intent
    3. Finally, extract data with intent-specific fields
    """
    try:
        # Get current date for relative date conversion
        today = datetime.now().strftime("%Y-%m-%d")

        # Step 1: Detect intent first with minimal schema
        intent_detection_schema = {
            "type": "object",
            "properties": {
                "intent": {
                    "type": "string",
                    "enum": CLINIC_INTENTS
                }
            },
            "required": ["intent"],
            "additionalProperties": False
        }

        intent_response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": "Detect the caller's intent from this medical clinic phone transcript. Return only JSON with intent field."
                },
                {
                    "role": "user",
                    "content": transcript
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "intent_detection",
                    "schema": intent_detection_schema,
                    "strict": True
                }
            }
        )

        intent_data = json.loads(intent_response.choices[0].message.content)
        detected_intent = intent_data["intent"]

        # Step 2: Build dynamic schema based on detected intent
        dynamic_schema = build_schema_for_intent(detected_intent)

        # Step 3: Extract all data with intent-specific fields
        full_response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a medical clinic phone assistant. Extract structured data from call transcripts.

TODAY'S DATE: {today}

Intent detected: {detected_intent}

IMPORTANT DATE CONVERSION RULES:
- "today" = {today}
- "tomorrow" = {(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")}
- "next week" = approximately {(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")}
- "next month" = approximately {(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")}
- If caller says a relative date, convert it to YYYY-MM-DD format using today's date as reference

Common field instructions:
- Extract name: the caller's full name. If not mentioned, use null
- Extract dob: date of birth in YYYY-MM-DD format (e.g., 1988-03-12). If not mentioned, use null
- Extract phone: the caller's callback phone number. If not mentioned, use null
- Extract summary: brief one-sentence summary of why they're calling
- Extract urgency: assess urgency level (low, medium, high, critical)
- Extract confidence: your confidence score (0.0-1.0) on accuracy of extraction

Intent-specific instructions:
{get_intent_instructions(detected_intent)}

Return ONLY the JSON data matching the schema."""
                },
                {
                    "role": "user",
                    "content": transcript
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "clinic_call_analysis",
                    "schema": dynamic_schema,
                    "strict": True
                }
            }
        )

        parsed_data = json.loads(full_response.choices[0].message.content)

        return {
            "success": True,
            "data": parsed_data
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

