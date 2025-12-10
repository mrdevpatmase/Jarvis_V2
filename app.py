from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from main import find_intent, execute_intent
from speech_text_transform import text_to_speech, speech_to_text
import os

from pymongo import MongoClient

MONGO_URI = "mongodb+srv://devpatmase1_db_user:JarvisDev123@cluster0.s0ayjkv.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["JarvisDB"]  # MongoDB will auto-create this
users_collection = db["users"]  # This is your users table


app = Flask(__name__)
app.secret_key = "super-secret-key"   # required for sessions & flash messages

# TEMP USER STORAGE (until DB is added)
USERS = {}     # structure: USERS["username"] = {full_name, email, password_hash}


# ------------------------------
# ROUTES FOR FRONTEND PAGES
# ------------------------------


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('welcome'))   # or 'home' if you want


@app.route('/welcome')
def home():
    return render_template('index.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ident = request.form.get("username_or_email")
        pwd = request.form.get("password")

        # Check username
        user = users_collection.find_one({"username": ident})

        # Or check email
        if not user:
            user = users_collection.find_one({"email": ident})

        if not user or not check_password_hash(user["password_hash"], pwd):
            flash("Invalid username/email or password.", "danger")
            return redirect(url_for("login"))

        session["user"] = user["username"]
        flash("Login successful!", "success")
        return redirect(url_for('home'))

    return render_template('login.html')




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        pwd = request.form.get("password")
        pwd2 = request.form.get("password2")

        if pwd != pwd2:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('signup'))

        # Check username
        if users_collection.find_one({"username": username}):
            flash("Username already taken.", "danger")
            return redirect(url_for('signup'))

        # Check email
        if users_collection.find_one({"email": email}):
            flash("Email already registered.", "danger")
            return redirect(url_for('signup'))

        password_hash = generate_password_hash(pwd)

        users_collection.insert_one({
            "full_name": full_name,
            "username": username,
            "email": email,
            "password_hash": password_hash
        })

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')



# ------------------------------
# JARVIS COMMAND ROUTES
# ------------------------------

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


# ------------------------------
# RUN SERVER
# ------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
