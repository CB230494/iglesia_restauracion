import streamlit as st
import pandas as pd
from db_ingresos import insertar_ingreso, obtener_ingresos

st.set_page_config(page_title="Sistema Iglesia Restauración", layout="centered")

# MENÚ SUPERIOR
menu = st.selectbox(
    "Selecciona una sección",
    [
        "📥 Registro de Ingresos",
        "💸 Registro de Gastos",
        "📊 Reporte General",
        "📄 Exportar PDF",
        "⚙️ Configuración"
    ]
)

# =================== PESTAÑA 1: REGISTRO DE INGRESOS =================== #
if menu == "📥 Registro de Ingresos":
    st.title("📥 Registro de Ingresos")

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

    st.subheader("📋 Ingresos registrados")
    datos = obtener_ingresos()

    if datos:
        df = pd.DataFrame(datos)
        if "monto" in df.columns:
            df["monto"] = df["monto"].map(lambda x: f"₡{x:,.2f}")
        st.table(df)
    else:
        st.info("No hay ingresos registrados todavía.")

# =================== PESTAÑA 2: REGISTRO DE GASTOS =================== #
elif menu == "💸 Registro de Gastos":
    st.title("💸 Registro de Gastos")
    st.warning("En construcción...")

# =================== PESTAÑA 3: REPORTE GENERAL =================== #
elif menu == "📊 Reporte General":
    st.title("📊 Reporte General")
    st.warning("En construcción...")

# =================== PESTAÑA 4: EXPORTAR PDF =================== #
elif menu == "📄 Exportar PDF":
    st.title("📄 Exportar reporte en PDF")
    st.warning("En construcción...")

# =================== PESTAÑA 5: CONFIGURACIÓN =================== #
elif menu == "⚙️ Configuración":
    st.title("⚙️ Configuración del sistema")
    st.warning("En construcción...")



