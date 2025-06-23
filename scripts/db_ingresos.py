from datetime import datetime
from supabase_client import supabase  # asegúrate de tenerlo

# === INGRESOS ===

def insertar_ingreso(fecha_date_obj, concepto, monto, observacion=""):
    fecha_str = fecha_date_obj.strftime("%d/%m/%Y")
    data = {
        "fecha": fecha_str,
        "concepto": concepto,
        "monto": monto,
        "observacion": observacion
    }
    supabase.table("ingresos").insert(data).execute()

def obtener_ingresos():
    response = supabase.table("ingresos").select("*").order("id", desc=True).execute()
    return response.data

def actualizar_ingreso(id, fecha_date_obj, concepto, monto, observacion):
    fecha_str = fecha_date_obj.strftime("%d/%m/%Y")
    supabase.table("ingresos").update({
        "fecha": fecha_str,
        "concepto": concepto,
        "monto": monto,
        "observacion": observacion
    }).eq("id", id).execute()

def eliminar_ingreso(id):
    supabase.table("ingresos").delete().eq("id", id).execute()


# === GASTOS ===

def insertar_gasto(fecha_date_obj, motivo, monto, observacion=""):
    fecha_str = fecha_date_obj.strftime("%d/%m/%Y")
    data = {
        "fecha": fecha_str,
        "motivo": motivo,
        "monto": monto,
        "observacion": observacion
    }
    supabase.table("gastos").insert(data).execute()

def obtener_gastos():
    response = supabase.table("gastos").select("*").order("id", desc=True).execute()
    return response.data

def actualizar_gasto(id, fecha_date_obj, motivo, monto, observacion):
    fecha_str = fecha_date_obj.strftime("%d/%m/%Y")
    supabase.table("gastos").update({
        "fecha": fecha_str,
        "motivo": motivo,
        "monto": monto,
        "observacion": observacion
    }).eq("id", id).execute()

def eliminar_gasto(id):
    supabase.table("gastos").delete().eq("id", id).execute()

