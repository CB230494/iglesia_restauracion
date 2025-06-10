import streamlit as st
import pandas as pd
from scripts.db_ingresos import (
    init_tables,
    insertar_ingreso,
    obtener_ingresos,
    actualizar_ingreso,
    eliminar_ingreso,
)

# Inicializar tablas
init_tables()

# Menú lateral
st.sidebar.title("📌 Navegación")
opcion = st.sidebar.radio("Ir a:", ["📥 Ingresos", "💸 Gastos", "📊 Reportes"])

# =====================================
# 📥 INGRESOS (REGISTRO Y GESTIÓN)
# =====================================
if opcion == "📥 Ingresos":
    st.title("📥 Ingresos - Iglesia Restauración")

    concepto = st.selectbox("Concepto", ["Diezmo", "Ofrenda", "Cocina", "Otro"], key="concepto_select")

    if concepto != "Cocina":
        with st.form("form_ingreso_normal"):
            monto = st.number_input("Monto (₡)", min_value=0.0, format="%.2f")
            observacion = st.text_area("Observación (opcional)")
            enviar = st.form_submit_button("Registrar Ingreso")

            if enviar:
                if monto > 0:
                    insertar_ingreso(concepto, monto, observacion)
                    st.success("✅ Ingreso registrado.")
                else:
                    st.error("❌ El monto debe ser mayor a 0.")

    else:
        st.subheader("🍽️ Cocina - Caja registradora")

        with st.form("form_cocina"):
            nombres = st.text_area("Productos (uno por línea)", placeholder="Ej: Refresco\nEmpanada")
            precios = st.text_area("Precios unitarios", placeholder="Ej: 500\n700")
            cantidades = st.text_area("Cantidades", placeholder="Ej: 2\n3")
            enviar = st.form_submit_button("Registrar Ingreso Cocina")

            if enviar:
                try:
                    nombres_list = nombres.strip().splitlines()
                    precios_list = [float(p) for p in precios.strip().splitlines()]
                    cantidades_list = [int(c) for c in cantidades.strip().splitlines()]

                    if len(nombres_list) != len(precios_list) or len(precios_list) != len(cantidades_list):
                        st.error("❌ Las listas deben tener el mismo número de elementos.")
                    else:
                        total = 0
                        detalle = []
                        for i in range(len(nombres_list)):
                            sub = precios_list[i] * cantidades_list[i]
                            total += sub
                            detalle.append(f"{cantidades_list[i]} x {nombres_list[i]} (₡{precios_list[i]:,.0f}) = ₡{sub:,.0f}")
                        obs = "\n".join(detalle)
                        insertar_ingreso("Cocina", total, obs)
                        st.success(f"✅ Cocina registrada (₡{total:,.0f})")
                except:
                    st.error("❌ Verifica que precios y cantidades sean numéricos.")

    # Mostrar ingresos registrados
    st.subheader("📋 Ingresos Registrados")
    ingresos = obtener_ingresos()
    df_ingresos = pd.DataFrame(ingresos, columns=["ID", "Fecha", "Concepto", "Monto", "Observación"])
    st.dataframe(df_ingresos, use_container_width=True)

    # CRUD: editar/eliminar
    st.subheader("✏️ Editar o Eliminar un ingreso")
    ingreso_ids = [str(i[0]) for i in ingresos]
    if ingreso_ids:
        selected_id = st.selectbox("Seleccionar ID", ingreso_ids)
        row = next(i for i in ingresos if str(i[0]) == selected_id)
        with st.form("edit_ingreso"):
            concepto_edit = st.selectbox("Concepto", ["Diezmo", "Ofrenda", "Cocina", "Otro"], index=["Diezmo", "Ofrenda", "Cocina", "Otro"].index(row[2]))
            monto_edit = st.number_input("Monto", value=row[3], min_value=0.0, format="%.2f")
            obs_edit = st.text_area("Observación", value=row[4])
            col1, col2 = st.columns(2)
            with col1:
                actualizar = st.form_submit_button("Actualizar")
            with col2:
                eliminar = st.form_submit_button("Eliminar")

            if actualizar:
                actualizar_ingreso(row[0], concepto_edit, monto_edit, obs_edit)
                st.success("✅ Ingreso actualizado correctamente.")
                st.experimental_rerun()

            if eliminar:
                eliminar_ingreso(row[0])
                st.warning("🗑️ Ingreso eliminado.")
                st.experimental_rerun()
    else:
        st.info("No hay ingresos registrados aún.")

