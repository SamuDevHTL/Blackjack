from flask import Flask, render_template, request, redirect, url_for
from mysql.connector import connect, Error

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT id, money FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                user_id, money = user
                # Pass user id and money to main page via query params (simple, not secure)
                return redirect(url_for("main", user_id=user_id))
            else:
                message = "Invalid username or password."

    return render_template("login.html", message=message)

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
                    # Insert user with starting money = 50
                    cursor.execute(
                        "INSERT INTO users (username, password, money) VALUES (%s, %s, %s)",
                        (username, password, 50)
                    )
                    conn.commit()
                    message = "Registration successful. You can now log in."
                    cursor.close()
                    conn.close()
                    return redirect(url_for("login"))
                except Error as e:
                    message = f"Registration failed: {e}"
            cursor.close()
            conn.close()

    return render_template("register.html", message=message)

@app.route("/main")
def main():
    user_id = request.args.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    conn = connect_db()
    money = 0
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT money FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            money = result[0]
        cursor.close()
        conn.close()

    return render_template("main.html", money=money)

if __name__ == "__main__":
    app.run(debug=True)

