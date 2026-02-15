# Test Cases for ScribeMD

Use these test transcripts to verify the AI intent detection is working correctly.

## Test Case 1: Urgent Medical Issue ⚠️ HIGH PRIORITY

**Input:**
```
Hi, this is Sarah Cohen, born 03/12/1988. I'm calling because I've had severe 
chest pain for the last two days and it's getting worse. I need to see a doctor 
urgently. Please call me back at 310-555-2211 as soon as possible.
```

**Expected Output:**
- Intent: `urgent_medical_issue`
- Urgency: `high` or `critical`
- Name: `Sarah Cohen`
- DOB: `1988-03-12`
- Phone: `310-555-2211`
- Symptoms: `["chest pain", "severe", "worsening"]`

---

## Test Case 2: Appointment Booking

**Input:**
```
Hello, my name is Michael Johnson and I was born on June 15, 1992. I'd like to 
schedule an appointment with Dr. Smith next Tuesday or Wednesday if possible. 
Can you call me back at 555-0147?
```

**Expected Output:**
- Intent: `appointment_booking`
- Urgency: `low`
- Name: `Michael Johnson`
- DOB: `1992-06-15`
- Phone: `555-0147`
- Appointment dates: `["next Tuesday", "next Wednesday"]`

---

## Test Case 3: Prescription Refill

**Input:**
```
Hi, this is Jennifer Martinez, my DOB is 1985-11-22. I need to refill my 
diabetes medication. I take Metformin twice a day. My callback number is 
(415) 555-0198.
```

**Expected Output:**
- Intent: `prescription_refill`
- Urgency: `low` or `medium`
- Name: `Jennifer Martinez`
- DOB: `1985-11-22`
- Phone: `(415) 555-0198`
- Medications: `["Metformin"]`

---

## Test Case 4: Lab Results

**Input:**
```
Hi, I'm David Lee, born 1979-03-08. I'm calling to check if my recent blood 
work results are ready. I had some tests done last week. Please reach me at 
206-555-0142.
```

**Expected Output:**
- Intent: `lab_results`
- Urgency: `low`
- Name: `David Lee`
- DOB: `1979-03-08`
- Phone: `206-555-0142`
- Other info: `["recent blood work", "tests done last week"]`

---

## Test Case 5: Billing Question

**Input:**
```
Hi, this is Linda Thompson born 1970-07-20. I received a bill for my recent 
visit and I have some questions about the charges. I don't think insurance 
covered everything. Call me back at 650-555-0123.
```

**Expected Output:**
- Intent: `billing_question`
- Urgency: `low`
- Name: `Linda Thompson`
- DOB: `1970-07-20`
- Phone: `650-555-0123`
- Other info: `["insurance coverage question", "billing discrepancy"]`

---

## Test Case 6: Insurance Question

**Input:**
```
Hello, this is Robert Kim, born August 3, 1988. I need to verify if the clinic 
is in-network with my insurance provider. My new insurance is Blue Shield. 
Please call me at 760-555-0191.
```

**Expected Output:**
- Intent: `insurance_question`
- Urgency: `low`
- Name: `Robert Kim`
- DOB: `1988-08-03`
- Phone: `760-555-0191`
- Other info: `["Blue Shield", "in-network verification"]`

---

## Test Case 7: Appointment Cancellation

**Input:**
```
Hi, this is Patricia Young, born 12/15/1965. I need to cancel my appointment 
on Thursday at 2 PM. Something came up and I won't be able to make it. My 
number is 775-555-0143.
```

**Expected Output:**
- Intent: `appointment_cancellation`
- Urgency: `low`
- Name: `Patricia Young`
- DOB: `1965-12-15`
- Phone: `775-555-0143`
- Appointment dates: `["Thursday", "2 PM"]`

---

## Test Case 8: Medication Side Effects

**Input:**
```
Hi, I'm Mark Richardson, DOB 1981-02-28. I started taking the new allergy 
medication Dr. Smith prescribed and I'm experiencing some dizziness and 
headaches. Should I stop taking it? Please call me at 971-555-0142.
```

**Expected Output:**
- Intent: `medication_side_effects`
- Urgency: `medium`
- Name: `Mark Richardson`
- DOB: `1981-02-28`
- Phone: `971-555-0142`
- Symptoms: `["dizziness", "headaches"]`
- Medications: `["allergy medication"]`

---

## How to Use These Test Cases

1. **Copy a test transcript** from above
2. **Paste into "Raw Transcript" field** in the web app
3. **Click "Submit"**
4. **Check if the parsed output matches expected values**
5. **Note any differences** (AI might phrase things differently)

---

## Tips for Better Results

1. **Include specific dates** - Makes date extraction more accurate
2. **Mention medications by name** - Improves medication detection
3. **Be clear about symptoms** - Use descriptive language
4. **Include callback number** - Helps with contact info extraction
5. **Provide date of birth** - Essential for patient identification

---

## Common Variations the AI Handles

The AI is smart enough to handle:
- ✅ Different date formats (03/12/1988, March 12, 1988, 1988-03-12)
- ✅ Phone number formats ((555) 123-4567, 555-123-4567, 5551234567)
- ✅ Casual language and filler words
- ✅ Multiple symptoms mentioned
- ✅ Implied urgency (e.g., "severe", "emergency", "ASAP")
- ✅ Missing information (returns null for missing fields)

