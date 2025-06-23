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

    # ------------------------ FORMULARIO PARA NUEVO INGRESO ------------------------
    st.subheader("Agregar nuevo ingreso")

    with st.form("form_nuevo_ingreso"):
        nueva_fecha = st.date_input("Fecha")
        nuevo_concepto = st.selectbox("Concepto", ["Diezmo", "Ofrenda", "Cocina", "Otro"])
        nuevo_monto = st.number_input("Monto (₡)", min_value=0.0, step=1000.0, format="%.2f")
        nueva_observacion = st.text_area("Observación (opcional)")
        enviar = st.form_submit_button("Registrar")

        if enviar:
            resultado = insertar_ingreso(str(nueva_fecha), nuevo_concepto, nuevo_monto, nueva_observacion)
            if resultado.data:
                st.success("✅ Ingreso registrado exitosamente")
                st.rerun()
            else:
                st.error(f"❌ Error al registrar: {resultado.error}")

    # ------------------------ LISTADO CON EDICIÓN Y ELIMINACIÓN ------------------------
    st.subheader("📋 Ingresos registrados")
    ingresos = obtener_ingresos()

    if ingresos:
        for ingreso in ingresos:
            with st.container():
                id_actual = ingreso['id']
                editando = st.session_state.get(f"edit_{id_actual}", False)

                if editando:
                    st.markdown(f"### ✏️ Editando ingreso ID {id_actual}")
                    fecha = st.date_input("Fecha", value=pd.to_datetime(ingreso["fecha"]), key=f"fecha_{id_actual}")
                    concepto = st.selectbox("Concepto", ["Diezmo", "Ofrenda", "Cocina", "Otro"],
                                            index=["Diezmo", "Ofrenda", "Cocina", "Otro"].index(ingreso["concepto"]),
                                            key=f"concepto_{id_actual}")
                    monto = st.number_input("Monto (₡)", min_value=0.0, value=float(ingreso["monto"]),
                                            format="%.2f", key=f"monto_{id_actual}")
                    observacion = st.text_input("Observación", value=ingreso["observacion"], key=f"obs_{id_actual}")
                    col1, col2 = st.columns([1, 1])
                    if col1.button("💾 Guardar", key=f"guardar_{id_actual}"):
                        actualizar_ingreso(id_actual, str(fecha), concepto, monto, observacion)
                        st.session_state[f"edit_{id_actual}"] = False
                        st.success("✅ Ingreso actualizado")
                        st.rerun()
                    if col2.button("❌ Cancelar", key=f"cancelar_{id_actual}"):
                        st.session_state[f"edit_{id_actual}"] = False
                        st.rerun()

                else:
                    cols = st.columns([1, 2, 2, 2, 3, 1, 1])
                    cols[0].markdown(f"**ID:** {ingreso['id']}")
                    cols[1].markdown(f"📅 {ingreso['fecha']}")
                    cols[2].markdown(f"📄 {ingreso['concepto']}")
                    cols[3].markdown(f"💰 ₡{ingreso['monto']:,.2f}")
                    cols[4].markdown(f"📝 {ingreso['observacion'] or '—'}")
                    if cols[5].button("✏️", key=f"editar_{id_actual}"):
                        st.session_state[f"edit_{id_actual}"] = True
                        st.rerun()
                    if cols[6].button("🗑️", key=f"eliminar_{id_actual}"):
                        eliminar_ingreso(id_actual)
                        st.success("✅ Ingreso eliminado")
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



