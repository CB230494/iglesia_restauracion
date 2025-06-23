from supabase_client import supabase

def insertar_gasto(fecha, concepto, monto, observacion=""):
    if not fecha or not concepto or monto is None:
        raise ValueError("❌ Todos los campos obligatorios deben completarse.")

    data = {
        "fecha": fecha.isoformat(),  # Aseguramos formato correcto
        "concepto": concepto.strip(),
        "monto": round(monto, 2),
        "observacion": observacion.strip() or None
    }

    print("📤 Enviando a Supabase (GASTO):", data)  # <- Ver en logs de Streamlit

    response = supabase.table("gastos").insert(data).execute()
    return response


def obtener_gastos():
    response = supabase.table("gastos").select("*").order("id", desc=True).execute()
    return response.data

def eliminar_gasto(id):
    response = supabase.table("gastos").delete().eq("id", id).execute()
    return response

def actualizar_gasto(id, fecha, concepto, monto, observacion=""):
    if not fecha or not concepto or monto is None:
        raise ValueError("❌ Todos los campos obligatorios deben completarse.")

    data = {
        "fecha": fecha.isoformat(),
        "concepto": concepto,
        "monto": monto,
        "observacion": observacion or None
    }

    response = supabase.table("gastos").update(data).eq("id", id).execute()
    return response
