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

    # ------------------------ FORMULARIO ------------------------
    st.subheader("Agregar o editar ingreso")

    if "modo_edicion" not in st.session_state:
        st.session_state.modo_edicion = False
    if "datos_edicion" not in st.session_state:
        st.session_state.datos_edicion = {}

    datos = st.session_state.datos_edicion if st.session_state.modo_edicion else {
        "fecha": None,
        "concepto": "Diezmo",
        "monto": 0.0,
        "observacion": ""
    }

    with st.form("form_ingreso"):
        fecha = st.date_input("Fecha", value=pd.to_datetime(datos["fecha"]) if datos["fecha"] else pd.to_datetime("today"))
        concepto = st.selectbox("Concepto", ["Diezmo", "Ofrenda", "Cocina", "Otro"], index=["Diezmo", "Ofrenda", "Cocina", "Otro"].index(datos["concepto"]))
        monto = st.number_input("Monto (₡)", min_value=0.0, value=float(datos["monto"]), step=1000.0, format="%.2f")
        observacion = st.text_area("Observación (opcional)", value=datos["observacion"])
        guardar = st.form_submit_button("Guardar")

        if guardar:
            if st.session_state.modo_edicion:
                res = actualizar_ingreso(datos["id"], str(fecha), concepto, monto, observacion)
                if res.data:
                    st.success("✅ Ingreso actualizado")
                else:
                    st.error("❌ No se pudo actualizar")
                st.session_state.modo_edicion = False
                st.session_state.datos_edicion = {}
                st.rerun()
            else:
                res = insertar_ingreso(str(fecha), concepto, monto, observacion)
                if res.data:
                    st.success("✅ Ingreso registrado")
                    st.rerun()
                else:
                    st.error("❌ Error al registrar")

    # ------------------------ LISTADO DE INGRESOS ------------------------
    st.subheader("📋 Ingresos registrados")
    ingresos = obtener_ingresos()

    if ingresos:
        for ingreso in ingresos:
            with st.container():
                cols = st.columns([1, 2, 2, 2, 3, 1, 1])
                cols[0].markdown(f"**ID:** {ingreso['id']}")
                cols[1].markdown(f"📅 {ingreso['fecha']}")
                cols[2].markdown(f"🧾 {ingreso['concepto']}")
                cols[3].markdown(f"💰 ₡{ingreso['monto']:,.2f}")
                cols[4].markdown(f"📝 {ingreso['observacion'] or '—'}")

                editar = cols[5].button("✏️", key=f"editar_{ingreso['id']}")
                eliminar = cols[6].button("🗑️", key=f"eliminar_{ingreso['id']}")

                if editar:
                    st.session_state.modo_edicion = True
                    st.session_state.datos_edicion = ingreso
                    st.rerun()

                if eliminar:
                    eliminar_ingreso(ingreso["id"])
                    st.success(f"Ingreso ID {ingreso['id']} eliminado")
                    st.rerun()
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



