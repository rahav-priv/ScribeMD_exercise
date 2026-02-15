# 🚀 HOW TO RUN SCRIBEMD

## Step 1: Get Your API Key

Choose one option:

### Option A: Anthropic Claude (Recommended - Easiest)
1. Go to: https://console.anthropic.com
2. Click "Sign Up" or "Sign In"
3. Go to "API Keys" section
4. Create new API key
5. Copy the key (looks like: `sk-ant-...`)

### Option B: OpenAI GPT
1. Go to: https://platform.openai.com/api-keys
2. Click "Sign Up" or "Sign In"
3. Create new API key
4. Copy the key (looks like: `sk-proj-...`)

---

## Step 2: Add API Key to .env File

**Open the .env file:**
```
/Users/rahavyairi/projects/scribemd/.env
```

**If using Anthropic Claude:**
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
```

**If using OpenAI:**
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
```

(Replace the `sk-ant-...` or `sk-proj-...` with your actual key)

---

## Step 3: Run the App

**Open Terminal and run:**
```bash
cd /Users/rahavyairi/projects/scribemd
./start.sh
```

**You should see:**
```
 * Running on http://localhost:5001
 * Debug mode: on
```

If you see any errors, scroll up to see what went wrong.

---

## Step 4: Open in Browser

**Go to:** http://localhost:5001

You should see the ScribeMD app with:
- Logo at the top
- "Transcript Parser: by Rahav Yairi" subtitle
- Left panel: "Raw Transcript" input box
- Right panel: "Parsed Data" output box
- Submit and Clear buttons

---

## Step 5: Test It!

Paste this example into the "Raw Transcript" field:

```
Hi, this is Sarah Cohen, born 03/12/1988. I've had severe chest pain 
for two days and it's getting worse. I need to see a doctor urgently. 
Please call me back at 310-555-2211.
```

Click "Submit" and you should see JSON output in the "Parsed Data" field showing:
- Intent: urgent_medical_issue
- Name: Sarah Cohen
- DOB: 1988-03-12
- Phone: 310-555-2211
- Urgency: high
- And more...

---

## ⚠️ Troubleshooting

### "Cannot find http://localhost:5001"
- Make sure you ran `./start.sh` and it says "Running on http://localhost:5001"
- Wait 5 seconds after seeing that message
- Try refreshing the browser (Cmd+R)

### "API key not configured" error
- Check that you edited the .env file correctly
- Make sure your API key is on the same line as ANTHROPIC_API_KEY= or OPENAI_API_KEY=
- Don't include quotes around the key
- Save the file (Cmd+S in most editors)

### "ModuleNotFoundError: No module named 'anthropic'"
- Run: `pip install anthropic`
- Then try `./start.sh` again

### Flask won't start
- Try: `python -m pip install --upgrade pip`
- Then: `pip install -r requirements.txt`
- Then: `./start.sh`

---

## 📞 Quick Reference

**Project Location:**
```
/Users/rahavyairi/projects/scribemd/
```

**Start Server:**
```
./start.sh
```

**Access App:**
```
http://localhost:5001
```

**API Endpoint:**
```
POST http://localhost:5001/api/parse
```

**To Stop Server:**
```
Ctrl+C in terminal
```

---

## ✅ You're Ready!

Your AI clinic phone assistant is set up and ready to analyze transcripts! 🎉

