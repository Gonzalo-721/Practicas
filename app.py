# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template
import psycopg2
from datetime import datetime

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST")      
DB_NAME = os.environ.get("DB_NAME")      
DB_USER = os.environ.get("DB_USER")      
DB_PASS = os.environ.get("DB_PASS")      
DB_PORT = int(os.environ.get("DB_PORT", 5432))

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        client_encoding="UTF8",
        sslmode='require' if DB_HOST != "localhost" else 'disable'
    )
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print("Error al conectar:", e)
    conn = None

@app.route("/")
def index():
    try:
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        hora = cur.fetchone()[0]
        cur.close()
    except Exception as e:
        hora = f"Error consultando la hora: {e}"
    return render_template("index.html", hora=hora)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
