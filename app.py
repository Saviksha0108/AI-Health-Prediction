from flask import Flask, render_template, request, redirect, url_for
from database import create_table, get_all_patients, add_patient, update_patient, delete_patient
from datetime import datetime, date
import re
import os
import time
import math
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ---------------- Gemini integration ----------------

GEMINI_MODEL = "gemini-3.5-flash-lite"
_BASE = "https://generativelanguage.googleapis.com/v1beta"


def _build_prompt(glucose, haemoglobin, cholesterol):
    return f"""
Analyze these patient blood test readings:

Glucose: {glucose} mg/dL
Haemoglobin: {haemoglobin} g/dL
Total Cholesterol: {cholesterol} mg/dL

Provide exactly three short, complete bullet points:
1. Glucose interpretation and possible risk. Mention that interpretation depends on fasting or random testing.
2. Haemoglobin interpretation and possible concern.
3. Cholesterol interpretation and possible cardiovascular risk.

Use cautious language. Do not diagnose or prescribe medication.
Do not leave sentences unfinished.
End with: Consult a healthcare professional for proper evaluation.
"""


def _extract_interactions_text(data):
    texts = []

    for step in data.get("steps", []):
        if step.get("type") == "model_output":
            for part in step.get("content", []):
                if part.get("type") == "text":
                    text = part.get("text", "").strip()
                    if text:
                        texts.append(text)

    return "\n".join(texts).strip()


def generate_health_remarks(glucose, haemoglobin, cholesterol):

    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini API key is missing. Check your .env file.")

    prompt = _build_prompt(glucose, haemoglobin, cholesterol)

    response = requests.post(
        f"{_BASE}/interactions",
        headers={
            "x-goog-api-key": GEMINI_API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "model": GEMINI_MODEL,
            "input": prompt,
            "store": False,
            "generation_config": {
                "max_output_tokens": 600
            }
        },
        timeout=60
    )

    if response.status_code != 200:
        print("[Gemini] API error:", response.status_code, response.text)
        raise RuntimeError(
            f"Gemini API failed with HTTP {response.status_code}. "
            "Please try again later."
        )

    result = response.json()
    remarks = _extract_interactions_text(result)

    if not remarks or result.get("status") != "completed":
        raise RuntimeError("Gemini returned an empty or incomplete response.")

    print("[Gemini] Successfully generated health remarks.")
    return remarks

# ---------------- Flask app ----------------

app = Flask(__name__)
create_table()


def validate_email(email):
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email)


@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/add")
def add_page():
    return render_template("index.html")


@app.route("/patients")
def patients():
    records = get_all_patients()
    return render_template("patients.html", patients=records)


@app.route("/add_patient", methods=["POST"])
def add_patient_route():
    full_name = request.form.get("full_name", "").strip()
    dob = request.form.get("dob", "").strip()
    email = request.form.get("email", "").strip()
    glucose = request.form.get("glucose", "").strip()
    haemoglobin = request.form.get("haemoglobin", "").strip()
    cholesterol = request.form.get("cholesterol", "").strip()

    error = None

    if not all([full_name, dob, email, glucose, haemoglobin, cholesterol]):
        error = "All fields are required."

    elif not validate_email(email):
        error = "Please enter a valid email address."

    else:
        parsed_date = None

        for fmt in ("%d/%m/%Y", "%d.%m.%Y"):
            try:
                parsed_date = datetime.strptime(dob, fmt).date()
                break
            except ValueError:
                pass

        if parsed_date is None:
            error = "Invalid date. Use DD/MM/YYYY."
        elif parsed_date > date.today():
            error = "Date of birth cannot be in the future."

    if not error:
        try:
            glucose_value = float(glucose)
            haemoglobin_value = float(haemoglobin)
            cholesterol_value = float(cholesterol)

            values = (glucose_value, haemoglobin_value, cholesterol_value)

            if not all(math.isfinite(v) for v in values):
                error = "Glucose, haemoglobin and cholesterol must be valid numbers."
            elif min(values) < 0:
                error = "Health values cannot be negative."

        except ValueError:
            error = "Glucose, haemoglobin and cholesterol must be numbers."

    if not error:
        for patient in get_all_patients():
            if (
                patient["full_name"].strip().lower() == full_name.lower()
                and patient["dob"] == dob
                and patient["email"].lower() == email.lower()
                and float(patient["glucose"]) == glucose_value
                and float(patient["haemoglobin"]) == haemoglobin_value
                and float(patient["cholesterol"]) == cholesterol_value
            ):
                error = "This patient record already exists."
                break

    if error:
        return render_template("index.html", error=error)

    try:
        remarks = generate_health_remarks(
        glucose_value,
        haemoglobin_value,
        cholesterol_value
    )
    except Exception as e:
        print("[AI ERROR]", str(e))
        return render_template(
        "index.html",
        error="AI analysis is temporarily unavailable. Please try again."
    )

    add_patient(
        full_name,
        dob,
        email,
        glucose_value,
        haemoglobin_value,
        cholesterol_value,
        remarks
    )

    return redirect(url_for("patients"))


@app.route("/edit/<int:patient_id>", methods=["POST"])
def edit_patient(patient_id):
    email = request.form.get("email", "").strip()

    if not validate_email(email):
        return "Please enter a valid email address.", 400

    update_patient(patient_id, email)
    return redirect(url_for("patients"))


@app.route("/delete/<int:patient_id>", methods=["POST"])
def remove_patient(patient_id):
    delete_patient(patient_id)
    return redirect(url_for("patients"))


if __name__ == "__main__":
    app.run(debug=True)