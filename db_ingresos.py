from supabase_client import supabase

def insertar_ingreso(fecha, concepto, monto, observacion=""):
    data = {
        "fecha": fecha,
        "concepto": concepto,
        "monto": monto,
        "observacion": observacion
    }
    response = supabase.table("ingresos").insert(data).execute()
    return response

def obtener_ingresos():
    response = supabase.table("ingresos").select("*").order("id", desc=True).execute()
    return response.data

def eliminar_ingreso(id):
    response = supabase.table("ingresos").delete().eq("id", id).execute()
    return response

def actualizar_ingreso(id, fecha, concepto, monto, observacion=""):
    data = {
        "fecha": fecha,
        "concepto": concepto,
        "monto": monto,
        "observacion": observacion
    }
    response = supabase.table("ingresos").update(data).eq("id", id).execute()
    return response
from supabase_client import supabase

def insertar_gasto(fecha, concepto, monto, observacion=""):
    data = {
        "fecha": fecha,
        "concepto": concepto,
        "monto": monto,
        "observacion": observacion
    }
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

