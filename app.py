
import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

APP_TOKEN = os.environ.get("JARVIS_APP_TOKEN")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "assistant": "JARVIS 3.0"
    })


@app.route("/chat", methods=["POST"])
def chat():
    if not APP_TOKEN:
        return jsonify({"error": "Server configuration missing"}), 500

    auth = request.headers.get("Authorization", "")
    if auth != "Bearer " + APP_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message or len(message) > 4000:
        return jsonify({"error": "Invalid message"}), 400

    try:
        result = client.responses.create(
            model="gpt-5.5",
            instructions="You are JARVIS, a friendly personal AI assistant.",
            input=message,
            max_output_tokens=500
        )
        return jsonify({"reply": result.output_text})

    except Exception:
        app.logger.exception("OpenAI error")
        return jsonify({"error": "AI service unavailable"}), 502
      
