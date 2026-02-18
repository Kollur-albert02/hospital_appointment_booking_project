from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "otp_secret_key"


# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    conn = sqlite3.connect("hospital.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- SPECIALIST SELECTION ----------------
@app.route("/schedule")
def schedule():
    return render_template("schedule.html")


# ---------------- DOCTORS BY SPECIALIST ----------------
@app.route("/doctors/<specialist>")
def doctors(specialist):

    doctor_data = {
        "physician": [
            {"name": "Dr. Anil Kumar", "qualification": "MD (General Medicine)", "experience": "12 Years"},
            {"name": "Dr. Sneha Rao", "qualification": "MBBS, MD", "experience": "8 Years"},
            {"name": "Dr. Rajesh Verma", "qualification": "MD (Internal Medicine)", "experience": "15 Years"},
            {"name": "Dr. Meena Sharma", "qualification": "MBBS, DNB", "experience": "10 Years"}
        ],
        "dermatologist": [
            {"name": "Dr. Pooja Malhotra", "qualification": "MD Dermatology", "experience": "7 Years"},
            {"name": "Dr. Rakesh Singh", "qualification": "MBBS, MD", "experience": "13 Years"},
            {"name": "Dr. Ananya Gupta", "qualification": "MD Dermatology", "experience": "10 Years"},
            {"name": "Dr. Vikram Joshi", "qualification": "MBBS, DDVL", "experience": "16 Years"}
        ],
        "cardiologist": [
            {"name": "Dr. Arjun Reddy", "qualification": "DM Cardiology", "experience": "14 Years"},
            {"name": "Dr. Kavita Nair", "qualification": "MD, DM Cardiology", "experience": "11 Years"},
            {"name": "Dr. Suresh Iyer", "qualification": "DM Cardiology", "experience": "18 Years"},
            {"name": "Dr. Neha Kapoor", "qualification": "MD Cardiology", "experience": "9 Years"}
        ],
        "neurologist": [
            {"name": "Dr. Sanjay Menon", "qualification": "DM Neurology", "experience": "20 Years"},
            {"name": "Dr. Priya Das", "qualification": "MD, DM Neurology", "experience": "12 Years"},
            {"name": "Dr. Rohit Bansal", "qualification": "DM Neurology", "experience": "9 Years"},
            {"name": "Dr. Nisha Kulkarni", "qualification": "MD Neurology", "experience": "14 Years"}
        ],
        "other": [
            {"name": "Dr. General A", "qualification": "MBBS", "experience": "5 Years"},
            {"name": "Dr. General B", "qualification": "MBBS", "experience": "6 Years"},
            {"name": "Dr. General C", "qualification": "MBBS", "experience": "4 Years"},
            {"name": "Dr. General D", "qualification": "MBBS", "experience": "8 Years"}
        ]
    }

    return render_template(
        "doctors.html",
        specialist=specialist,
        doctors=doctor_data.get(specialist, [])
    )


# ---------------- BOOK APPOINTMENT ----------------
@app.route("/book", methods=["GET", "POST"])
def book_appointment():

    if request.method == "POST":
        session["patient_data"] = {
            "patient_name": request.form["name"],
            "age": request.form["age"],
            "address": request.form["address"],
            "phone": request.form["phone"],
            "health_condition": request.form["condition"],
            "doctor_name": request.form["doctor"]
        }

        otp = random.randint(100000, 999999)
        session["otp"] = str(otp)

        print("OTP (Demo):", otp)

        return redirect(url_for("verify_otp"))

    return render_template("book.html")


# ---------------- OTP VERIFICATION ----------------
@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    if request.method == "POST":
        if request.form["otp"] == session.get("otp"):

            data = session.get("patient_data")
            conn = get_db_connection()

            # ✅ STORE ALL DATA (NO DELETE)
            conn.execute("""
                INSERT INTO appointments
                (patient_name, age, address, phone, health_condition, doctor_name)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data["patient_name"],
                data["age"],
                data["address"],
                data["phone"],
                data["health_condition"],
                data["doctor_name"]
            ))

            conn.commit()
            conn.close()
            session.clear()

            return redirect(url_for("history"))

        return render_template("verify_otp.html", error="Invalid OTP")

    return render_template("verify_otp.html")


# ---------------- SUCCESS PAGE ----------------
@app.route("/success")
def success():
    return render_template("success.html")


# ---------------- APPOINTMENT HISTORY (LATEST ONLY) ----------------
@app.route("/history")
def history():
    conn = get_db_connection()

    appointment = conn.execute("""
        SELECT * FROM appointments
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()

    conn.close()
    return render_template("history.html", appointment=appointment)


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
