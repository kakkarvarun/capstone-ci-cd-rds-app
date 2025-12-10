import os
import psycopg2
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "userdb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "SuperSecureP@ssw0rd123"),
    )
    return conn


def init_db():
    """Create the users table if it does not exist."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE
        );
        """
    )
    conn.commit()
    cur.close()
    conn.close()


@app.before_first_request
def setup_db():
    """
    This runs once per app instance (per container) before the first request.
    In ECS this ensures the users table exists in RDS so /users won't 500.
    """
    try:
        init_db()
    except Exception as e:
        # Log the error – you’ll see this in CloudWatch if something goes wrong
        app.logger.error("Failed to initialize database: %s", e)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@app.route("/users", methods=["GET"])
def list_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, first_name, last_name, email FROM users ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    users = [
        {"id": r[0], "first_name": r[1], "last_name": r[2], "email": r[3]}
        for r in rows
    ]
    return jsonify(users)


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, first_name, last_name, email FROM users WHERE id = %s;",
        (user_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row is None:
        return jsonify({"error": "User not found"}), 404
    user = {"id": row[0], "first_name": row[1], "last_name": row[2], "email": row[3]}
    return jsonify(user)


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(force=True)
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")

    if not first_name or not last_name:
        return jsonify({"error": "first_name and last_name are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO users (first_name, last_name, email)
        VALUES (%s, %s, %s)
        RETURNING id;
        """,
        (first_name, last_name, email),
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(
        {
            "id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        }
    ), 201


if __name__ == "__main__":
    # For local runs: make sure table exists before starting Flask dev server
    init_db()
    app.run(host="0.0.0.0", port=5000)
