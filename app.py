from flask import Flask, render_template, request, jsonify

    app.run(debug=True, host='localhost', port=5000)
if __name__ == '__main__':

    return jsonify(parsed_data)
    
    }
        # Add more parsed fields here later
        'raw_transcript': raw_transcript,
    parsed_data = {
    # This is where you'll add parsing logic later
    # Basic parsing - for now just return the raw transcript
    
    raw_transcript = data.get('transcript', '')
    data = request.get_json()
    """
    Later, parsing rules can be added here.
    For now, the parsed data contains just the raw transcript itself.
    Receives raw transcript from frontend and returns parsed JSON data.
    """
def parse_transcript():
@app.route('/api/parse', methods=['POST'])

    return render_template('index.html')
def index():
@app.route('/')

app = Flask(__name__)

import json
