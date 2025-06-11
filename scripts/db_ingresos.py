import sqlite3
from datetime import datetime

DB_PATH = "db.sqlite"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

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

def insertar_ingreso(fecha_date_obj, concepto, monto, observacion=""):
    """
    fecha_date_obj: tipo datetime.date (formato de Streamlit date_input)
    """
    fecha_str = fecha_date_obj.strftime("%d/%m/%Y")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ingresos (fecha, concepto, monto, observacion) VALUES (?, ?, ?, ?)",
                   (fecha_str, concepto, monto, observacion))
    conn.commit()
    conn.close()

def obtener_ingresos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ingresos ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def actualizar_ingreso(id, fecha_date_obj, concepto, monto, observacion):
    fecha_str = fecha_date_obj.strftime("%d/%m/%Y")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ingresos SET fecha = ?, concepto = ?, monto = ?, observacion = ? WHERE id = ?",
                   (fecha_str, concepto, monto, observacion, id))
    conn.commit()
    conn.close()

def eliminar_ingreso(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ingresos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

