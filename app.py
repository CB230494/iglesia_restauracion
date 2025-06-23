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
from db_ingresos import insertar_ingreso, obtener_ingresos, eliminar_ingreso, actualizar_ingreso

if menu == "📥 Registro de Ingresos":
    st.title("📥 Registro de Ingresos")

    # ================= FORMULARIO DE AGREGAR O EDITAR =================
    st.subheader("Agregar / Editar ingreso")

    if "modo_edicion" not in st.session_state:
        st.session_state.modo_edicion = False
    if "datos_edicion" not in st.session_state:
        st.session_state.datos_edicion = {}

    if st.session_state.modo_edicion:
        datos = st.session_state.datos_edicion
        st.info(f"✏️ Editando ingreso ID {datos['id']}")
    else:
        datos = {"fecha": None, "concepto": "Diezmo", "monto": 0.0, "observacion": ""}

    with st.form("formulario_ingreso"):
        fecha = st.date_input("Fecha", value=pd.to_datetime(datos["fecha"]) if datos["fecha"] else pd.to_datetime("today"))
        concepto = st.selectbox("Concepto", ["Diezmo", "Ofrenda", "Cocina", "Otro"], index=["Diezmo", "Ofrenda", "Cocina", "Otro"].index(datos["concepto"]) if datos["concepto"] else 0)
        monto = st.number_input("Monto (₡)", min_value=0.0, value=float(datos["monto"]), step=1000.0, format="%.2f")
        observacion = st.text_area("Observación (opcional)", value=datos["observacion"])
        enviar = st.form_submit_button("Guardar")

        if enviar:
            if st.session_state.modo_edicion:
                resultado = actualizar_ingreso(datos["id"], str(fecha), concepto, monto, observacion)
                if resultado.data:
                    st.success("✅ Ingreso actualizado")
                else:
                    st.error("❌ Error al actualizar")
                st.session_state.modo_edicion = False
                st.session_state.datos_edicion = {}
                st.experimental_rerun()
            else:
                resultado = insertar_ingreso(str(fecha), concepto, monto, observacion)
                if resultado.data:
                    st.success("✅ Ingreso registrado")
                    st.experimental_rerun()
                else:
                    st.error("❌ Error al registrar")

    # ================= TABLA CON OPCIONES DE EDITAR Y ELIMINAR =================
    st.subheader("📋 Ingresos registrados")
    ingresos = obtener_ingresos()

    if ingresos:
        for ingreso in ingresos:
            col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 2, 2, 1])
            col1.write(f"ID: {ingreso['id']}")
            col2.write(ingreso["fecha"])
            col3.write(ingreso["concepto"])
            col4.write(f"₡{ingreso['monto']:,.2f}")
            col5.write(ingreso["observacion"] or "")
            editar = col6.button("✏️", key=f"editar_{ingreso['id']}")
            eliminar = col6.button("🗑️", key=f"eliminar_{ingreso['id']}")

            if editar:
                st.session_state.modo_edicion = True
                st.session_state.datos_edicion = ingreso
                st.experimental_rerun()

            if eliminar:
                eliminar_ingreso(ingreso["id"])
                st.success(f"✅ Ingreso ID {ingreso['id']} eliminado")
                st.experimental_rerun()
    else:
        st.info("No hay ingresos registrados.")


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



