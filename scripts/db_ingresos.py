import sqlite3
from datetime import datetime

DB_PATH = "db.sqlite"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# === CREACIÓN DE TABLAS ===

def init_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla de ingresos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingresos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            concepto TEXT NOT NULL,
            monto REAL NOT NULL,
            observacion TEXT
        )
    ''')

    # Tabla de gastos
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

# === FUNCIONES PARA INGRESOS ===

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

def obtener_ingresos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ingresos ORDER BY fecha DESC")
    data = cursor.fetchall()
    conn.close()
    return data

# === FUNCIONES PARA GASTOS ===

def insertar_gasto(motivo, monto, observacion=""):
    conn = get_connection()
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT INTO gastos (fecha, motivo, monto, observacion)
        VALUES (?, ?, ?, ?)
    ''', (fecha_actual, motivo, monto, observacion))
    conn.commit()
    conn.close()

def obtener_gastos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gastos ORDER BY fecha DESC")
    data = cursor.fetchall()
    conn.close()
    return data
