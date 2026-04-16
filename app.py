import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


# ----------------------------------------------------
# DATABASE INITIALIZATION
# ----------------------------------------------------
def init_db():

    conn = sqlite3.connect("calculator.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num1 REAL,
            num2 REAL,
            result REAL
        )
    """)

    conn.commit()
    conn.close()


init_db()


# ----------------------------------------------------
# HOME ROUTE (CALCULATOR)
# ----------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():

    result = None

    conn = sqlite3.connect("calculator.db")
    cursor = conn.cursor()

    # GET HISTORY (always show updated history)
    cursor.execute("SELECT num1, num2, result FROM history ORDER BY id DESC")
    history = cursor.fetchall()

    if request.method == 'POST':

        num1 = request.form.get('number1', type=float)
        num2 = request.form.get('number2', type=float)

        if num1 is not None and num2 is not None:

            result = num1 + num2

            # SAVE TO DATABASE
            cursor.execute(
                "INSERT INTO history (num1, num2, result) VALUES (?, ?, ?)",
                (num1, num2, result)
            )

            conn.commit()

            # refresh history after insert
            cursor.execute("SELECT num1, num2, result FROM history ORDER BY id DESC")
            history = cursor.fetchall()

    conn.close()

    return render_template('index.html', result=result, history=history)


# ----------------------------------------------------
# CLEAR HISTORY ROUTE
# ----------------------------------------------------
@app.route('/clear-history', methods=['POST'])
def clear_history():

    conn = sqlite3.connect("calculator.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history")  # delete all records

    conn.commit()
    conn.close()

    return redirect('/')  # go back to homepage


# ----------------------------------------------------
# RUN SERVER
# ----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)