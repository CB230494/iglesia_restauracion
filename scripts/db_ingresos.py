import sqlite3
from datetime import datetime

DB_PATH = "db.sqlite"  # Guardar directamente en la raíz

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_ingresos_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingresos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            concepto TEXT NOT NULL,
            monto REAL NOT NULL,
            observacion TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insertar_ingreso(concepto, monto, observacion=""):
    conn = get_connection()
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT INTO ingresos (fecha, concepto, monto, observacion)
        VALUES (?, ?, ?, ?)
    ''', (fecha_actual, concepto, monto, observacion))
    conn.commit()
    conn.close()
