from flask import Flask, render_template, request, jsonify
from main import find_intent, execute_intent
from speech_text_transform import text_to_speech, speech_to_text
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route("/give_command", methods=['POST'])
# def give_command():
#     data = request.get_json()
#     command = data.get("command", "").strip()

#     if not command:
#         return jsonify({"status": "No command received."})

#     print(f"🎤 Command received: {command}")
#     intent = find_intent(command)
#     execute_intent(intent)
#     return jsonify({"status": f"Executed intent: {intent}"})


@app.route("/give_command", methods=['POST'])
def give_command():
    data = request.get_json()
    command = data.get("command", "").strip()

    if not command:
        return jsonify({"status": "No command received."})

    print(f"🎤 Command received: {command}")
    intent = find_intent(command)
    response_text = execute_intent(intent)

    return jsonify({"status": response_text})



@app.route("/stop_command", methods=['POST'])
def stop_command():
    print("🛑 Jarvis received stop request")
    return jsonify({"status": "Jarvis has stopped listening."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
