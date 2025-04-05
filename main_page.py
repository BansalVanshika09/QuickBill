from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

EXCEL_FILE = 'users.xlsx'

# Ensure Excel file exists with Name & Mobile Number columns
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['Name', 'Mobile Number'])
    df.to_excel(EXCEL_FILE, index=False)

# 📌 Home Page → Uses `main.html`
@app.route('/')
def main():
    return render_template('app.html')
@app.route('/customer')
def customer():
    return render_template('customer.html')
# 📌 Signup Page → Uses `form.html`
@app.route('/form')
def signup_form():
    return render_template('form.html')

# 📌 Signup Route (Handles Form Submission)
@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    mobile_number = request.form.get('mobile_number')

    df = pd.read_excel(EXCEL_FILE)

    # Check if mobile number is already registered
    if mobile_number in df['Mobile Number'].astype(str).values:
        return "Mobile number already registered."

    # Append new user
    new_user = pd.DataFrame([[name, mobile_number]], columns=df.columns)
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

    return redirect(url_for('main'))  # Redirect to Home Page after signup

if __name__ == '__main__':
    app.run(debug=True)
