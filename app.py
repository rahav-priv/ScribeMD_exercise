from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/parse', methods=['POST'])
def parse_transcript():
    """
    Receives raw transcript from frontend and returns parsed JSON data.
    For now, the parsed data contains just the raw transcript itself.
    Later, parsing rules can be added here.
    """
    data = request.get_json()
    raw_transcript = data.get('transcript', '')

    # Basic parsing - for now just return the raw transcript
    # This is where you'll add parsing logic later
    parsed_data = {
        'raw_transcript': raw_transcript,
        # Add more parsed fields here later
    }

    return jsonify(parsed_data)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)

