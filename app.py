import sqlite3
from datetime import datetime

DB_PATH = "db.sqlite"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_tables():
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            motivo TEXT NOT NULL,
            monto REAL NOT NULL,
            observacion TEXT
        )
    ''')

    conn.commit()
    conn.close()

# === INGRESOS ===

def insertar_ingreso(concepto, monto, observacion=""):
    conn = get_connection()
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO ingresos (fecha, concepto, monto, observacion) VALUES (?, ?, ?, ?)",
                   (fecha, concepto, monto, observacion))
    conn.commit()
    conn.close()

def obtener_ingresos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ingresos ORDER BY fecha DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def actualizar_ingreso(id, concepto, monto, observacion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ingresos SET concepto = ?, monto = ?, observacion = ? WHERE id = ?",
                   (concepto, monto, observacion, id))
    conn.commit()
    conn.close()

def eliminar_ingreso(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ingresos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
