from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import os

# 🔥 IMPORT ONLY THE BRAIN (TEXT → TEXT)
from app.main import process_command

# ==============================
# DATABASE
# ==============================

MONGO_URI = "mongodb+srv://devpatmase1_db_user:JarvisDev123@cluster0.s0ayjkv.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["JarvisDB"]
users_collection = db["users"]

# ==============================
# FLASK APP
# ==============================

app = Flask(__name__)
app.secret_key = "super-secret-key"

# ==============================
# FRONTEND ROUTES
# ==============================

@app.route("/")
def welcome_page():
    return render_template("welcome.html")


@app.route("/home")
def home_page():
    return render_template("index.html")


@app.route("/guest")
def guest():
    session["user"] = "Guest"
    return redirect(url_for("home_page"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("welcome_page"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ident = request.form.get("username_or_email")
        pwd = request.form.get("password")

        user = users_collection.find_one({"username": ident}) or \
               users_collection.find_one({"email": ident})

        if not user or not check_password_hash(user["password_hash"], pwd):
            flash("Invalid credentials", "danger")
            return redirect(url_for("login"))

        session["user"] = user["username"]
        flash("Login successful!", "success")
        return redirect(url_for("home_page"))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        pwd = request.form.get("password")
        pwd2 = request.form.get("password2")

        if pwd != pwd2:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("signup"))

        if users_collection.find_one({"username": username}):
            flash("Username already exists.", "danger")
            return redirect(url_for("signup"))

        if users_collection.find_one({"email": email}):
            flash("Email already registered.", "danger")
            return redirect(url_for("signup"))

        users_collection.insert_one({
            "full_name": full_name,
            "username": username,
            "email": email,
            "password_hash": generate_password_hash(pwd)
        })

        flash("Account created. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

# ==============================
# JARVIS API (TEXT ONLY)
# ==============================

@app.route("/give_command", methods=["POST"])
def give_command():
    data = request.get_json()
    command = data.get("command", "").strip()

    if not command:
        return jsonify({"status": "No command received."})

    print(f"🌐 Web Command: {command}")

    # 🔥 SINGLE ENTRY POINT
    response = process_command(command)

    return jsonify({"status": response})


@app.route("/stop_command", methods=["POST"])
def stop_command():
    return jsonify({"status": "Jarvis stopped."})

# ==============================
# RUN SERVER (LOCALHOST)
# ==============================

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
