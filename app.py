
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)

# Allow your GitHub Pages website to connect
CORS(
    app,
    resources={
        r"/chat": {
            "origins": [
                "https://jaipal-0852.github.io"
            ]
        }
    }
)

# OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Private JARVIS app token
APP_TOKEN = os.environ.get("JARVIS_APP_TOKEN")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "assistant": "JARVIS 3.0"
    })


@app.route("/chat", methods=["POST"])
def chat():

    # Check server configuration
    if not APP_TOKEN:
        return jsonify({
            "error": "Server configuration missing"
        }), 500

    # Verify private app token
    auth = request.headers.get("Authorization", "")

    if auth != "Bearer " + APP_TOKEN:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    # Read user message
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message or len(message) > 4000:
        return jsonify({
            "error": "Invalid message"
        }), 400

    # Send message to OpenAI
    try:
        result = client.responses.create(
            model="gpt-5.5",
            instructions=(
                "You are JARVIS, a friendly personal AI assistant. "
                "Give clear, helpful and concise answers."
            ),
            input=message,
            max_output_tokens=500
        )

        return jsonify({
            "reply": result.output_text
        })

    except Exception:
        app.logger.exception("OpenAI error")

        return jsonify({
            "error": "AI service unavailable"
        }), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
