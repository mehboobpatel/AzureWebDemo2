import os
import pyodbc
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_connection():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    return pyodbc.connect(conn_str)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedbacks (name, message) VALUES (?, ?)",
            (name, message)
        )
        conn.commit()
        conn.close()

        return redirect("/feedbacks")

    return render_template("index.html")


@app.route("/feedbacks")
def feedbacks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, message, created_at FROM feedbacks ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    return render_template("feedbacks.html", feedbacks=rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=False)
