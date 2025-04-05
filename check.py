from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

# Ensure the Excel file exists
EXCEL_FILE = "users.xlsx"
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Name", "Phone Number"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route("/")
def index():
    return render_template("app.html")  # Main page of the site

@app.route("/customer")
def customer():
    return render_template("customer.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]

        # Print statements for debugging
        print(f"Received: Name={name}, Phone={phone}")

        # Load existing data
        df = pd.read_excel(EXCEL_FILE)

        # Append new user data
        new_user = pd.DataFrame[[name, phone]],  