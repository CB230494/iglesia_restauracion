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
    response = supabase.table("ingresos").select("*").execute()
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


