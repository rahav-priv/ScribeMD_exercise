# ScribeMD - Quick Setup Guide

## 1. Get Your API Key

You need an OpenAI API key to use this app. You can use either:

### Option A: Claude API (Recommended)
1. Go to https://console.anthropic.com
2. Sign up for an account
3. Create an API key
4. Add it to your `.env` file as `ANTHROPIC_API_KEY=your_key_here`

### Option B: OpenAI API
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Add it to your `.env` file as `OPENAI_API_KEY=your_key_here`

## 2. Configure Environment Variables

Copy the template and add your API key:

```bash
cp .env.example .env
# Then edit .env and add your actual API key
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the App

```bash
./start.sh
# or manually:
python app.py
```

## 5. Access the App

Open your browser and go to: **http://localhost:5001**

## 6. Test It Out

Paste a sample transcript like:

```
Hi, this is Sarah Cohen, born 03/12/1988. I need to book an appointment 
because I've had chest pain for two days. Please call me back at 310-555-2211.
```

Click "Submit" and watch the AI analyze it!

## Troubleshooting

### "OpenAI API key not configured"
- Make sure you created a `.env` file with your API key
- Check that the key is correct and has permissions

### "Port 5000 already in use"
- The app uses port 5001 by default (to avoid macOS AirPlay conflicts)
- If you need a different port, edit `app.py` and change the port number

### API Rate Limits
- If you get rate limit errors, wait a moment and try again
- OpenAI has rate limits based on your subscription tier

## Supported Call Types

The system can automatically detect:
- Appointment booking/cancellation/rescheduling
- Prescription refills
- Lab results inquiries
- Billing questions
- Insurance questions
- Medication side effects
- **Urgent medical issues** (flags high priority)
- General inquiries
- Referral requests
- Follow-up calls
- Test scheduling
- Record requests
- And more!

## Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Ensure your API key is valid
3. Check that the transcript format is clear and complete

