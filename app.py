from flask import Flask, render_template, request, redirect, url_for
from mysql.connector import connect, Error

app = Flask(__name__)

# Database connection function
def connect_db():
    try:
        return connect(
            host="localhost",
            user="samudev",
            password="pac",
            database="gambling"
        )
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# Login route
@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                return redirect(url_for("main"))
            else:
                message = "Invalid username or password."

    return render_template("login.html", message=message)

# Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                message = "Username already taken."
            else:
                try:
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                    conn.commit()
                    message = "Registration successful. You can now log in."
                    return redirect(url_for("login"))
                except Error as e:
                    message = f"Registration failed: {e}"
            cursor.close()
            conn.close()

    return render_template("register.html", message=message)

# Main page
@app.route("/main")
def main():
    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True)

