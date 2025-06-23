from supabase_client import supabase

def insertar_gasto(fecha, concepto, monto, observacion=""):
    data = {
        "fecha": fecha,  # debe ser datetime.date
        "concepto": concepto,
        "monto": monto,
        "observacion": observacion
    }
    print("📤 Insertando en gastos:", data)  # Opcional para depuración
    response = supabase.table("gastos").insert(data).execute()
    return response

def obtener_gastos():
    response = supabase.table("gastos").select("*").order("id", desc=True).execute()
    return response.data

def eliminar_gasto(id):
    response = supabase.table("gastos").delete().eq("id", id).execute()
    return response

def actualizar_gasto(id, fecha, concepto, monto, observacion=""):
    data = {
        "fecha": fecha,
        "concepto": concepto,
        "monto": monto,
        "observacion": observacion
    }
    response = supabase.table("gastos").update(data).eq("id", id).execute()
    return response
