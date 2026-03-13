from flask import Flask, request, jsonify
import os
from groq import Groq

app = Flask(__name__, static_folder='.')
# Initialize Groq client
# You can replace this string with your actual key, 
# or better yet, set it as an environment variable: os.environ.get("GROQ_API_KEY")
client = Groq(api_key="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")

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response

    data = request.json
    try:
        # Convert the system string into a system message for Groq
        messages = [{"role": "system", "content": data.get('system', '')}] + data.get('messages', [])
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Fast, free, open-source model
            messages=messages,
            max_tokens=1000,
            temperature=0.6
        )
        reply = response.choices[0].message.content
        r = jsonify({"reply": reply})
    except Exception as e:
        r = jsonify({"error": str(e)})
        r.status_code = 500

    r.headers.add("Access-Control-Allow-Origin", "*")
    return r

@app.route('/')
def index():
    return app.send_static_file('ai_agents.html')

if __name__ == '__main__':
    app.run(debug=True)
