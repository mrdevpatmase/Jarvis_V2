from flask import Flask, render_template, request, jsonify
from main import find_intent, execute_intent

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    command = request.form.get('command')
    intent = find_intent(command)
    execute_intent(intent)
    return jsonify({"intent": intent, "command": command})

if __name__ == '__main__':
    app.run(debug=True)
