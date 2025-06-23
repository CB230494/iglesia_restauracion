import streamlit as st
from db_ingresos import insertar_ingreso, obtener_ingresos

st.set_page_config(page_title="Registro de Ingresos", layout="centered")

st.title("📥 Registro de Ingresos - Iglesia Restauración")

# Formulario para ingresar un nuevo ingreso
st.subheader("Agregar nuevo ingreso")
with st.form("formulario_ingreso"):
    fecha = st.date_input("Fecha")
    concepto = st.selectbox("Concepto", ["Diezmo", "Ofrenda", "Cocina", "Otro"])
    monto = st.number_input("Monto (₡)", min_value=0.0, step=1000.0, format="%.2f")
    observacion = st.text_area("Observación (opcional)")
    enviar = st.form_submit_button("Registrar")

    if enviar:
        resultado = insertar_ingreso(str(fecha), concepto, monto, observacion)
        if resultado.data:
            st.success("✅ Ingreso registrado exitosamente")
            st.experimental_rerun()
        else:
            st.error(f"❌ Error al registrar: {resultado.error}")

# Mostrar los ingresos registrados
st.subheader("📋 Ingresos registrados")
datos = obtener_ingresos()
if datos:
    st.table(datos)
else:
    st.info("No hay ingresos registrados todavía.")


