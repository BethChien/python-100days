from flask import Flask, request, g, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def init_db():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """)
    conn.commit()

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            cursor_factory=RealDictCursor,
        )
        g.db.autocommit = False
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/", methods=["GET"])
def home():
    return "Hello World"

@app.route("/contacts", methods=["GET"])
def list_contacts():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS contacts (id SERIAL PRIMARY KEY, name TEXT, email TEXT, phone TEXT)")
        cur.execute("SELECT id, name, email, phone FROM contacts ORDER BY id")
        rows = cur.fetchall()
    return jsonify(rows)      

@app.route("/contacts", methods=["POST"])
def add_contact():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "invalid JSON body"}), 400

    name  = (data.get("name")  or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()

    if not name or not email or not phone:
        return jsonify({"error": "name, email, and phone are required"}), 400

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO contacts (name, email, phone)
                VALUES (%s, %s, %s)
                RETURNING id, name, email, phone
                """,
                (name, email, phone),
            )
            row = cur.fetchone()
        conn.commit()
        return jsonify(row), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "invalid JSON body"}), 400
    
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    
    if not name or not email or not phone:
        return jsonify({"error": "name, email, and phone are required"}), 400
    
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE contacts
                   SET name=%s, email=%s, phone=%s
                 WHERE id=%s
             RETURNING id, name, email, phone
            """, (name, email, phone, contact_id))
            row = cur.fetchone()
        conn.commit()
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"error": "contact not found"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM contacts WHERE id = %s RETURNING id", (contact_id,))
            deleted = cur.fetchone()
        conn.commit()
    
        if deleted:
            return jsonify({"status": "deleted", "id": contact_id}), 200
        else:
            return jsonify({"error": "contacr not found"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)