import streamlit as st
import pandas as pd
from datetime import date
from scripts.db_ingresos import (
    init_tables,
    insertar_ingreso,
    obtener_ingresos,
    actualizar_ingreso,
    eliminar_ingreso
)

# Inicializar base de datos
init_tables()

# Menú lateral
st.sidebar.title("📌 Navegación")
opcion = st.sidebar.radio("Ir a:", ["📥 Ingresos", "💸 Gastos", "📊 Reportes"])

# =====================================
# 📥 INGRESOS - IGLESIA RESTAURACIÓN COLONIA CARVAJAL
# =====================================
if opcion == "📥 Ingresos":
    st.title("📥 Registro de Ingresos - Iglesia Restauración Colonia Carvajal")

    concepto = st.selectbox("Concepto", ["Diezmo", "Ofrenda", "Cocina", "Otro"], key="concepto_select")

    # ====================
    # INGRESO NORMAL
    # ====================
    if concepto != "Cocina":
        st.markdown("### ➕ Nuevo ingreso")
        with st.form("form_ingreso_normal"):
            col1, col2 = st.columns(2)
            with col1:
                fecha = st.date_input("Fecha del ingreso", value=date.today())
                st.markdown(f"📅 Fecha seleccionada: **{fecha.strftime('%d/%m/%Y')}**")
                monto = st.number_input("Monto (₡)", min_value=0.0, format="%.2f")
            with col2:
                concepto_display = st.text_input("Concepto", value=concepto, disabled=True)
                observacion = st.text_area("Observación (opcional)")

            enviar = st.form_submit_button("Registrar Ingreso")

            if enviar:
                if monto > 0:
                    insertar_ingreso(fecha, concepto, monto, observacion)
                    st.success("✅ Ingreso registrado correctamente.")
                    st.rerun()
                else:
                    st.error("❌ El monto debe ser mayor a 0.")

    # ====================
    # INGRESO COCINA (CAJA)
    # ====================
    else:
        st.markdown("### 🍽️ Cocina - Caja registradora")
        with st.form("form_cocina"):
            col1, col2 = st.columns(2)
            with col1:
                fecha = st.date_input("Fecha de la venta", value=date.today())
                st.markdown(f"📅 Fecha seleccionada: **{fecha.strftime('%d/%m/%Y')}**")
                nombres = st.text_area("Productos (uno por línea)", placeholder="Ej: Refresco\nEmpanada")
            with col2:
                precios = st.text_area("Precios unitarios", placeholder="Ej: 500\n700")
                cantidades = st.text_area("Cantidades", placeholder="Ej: 2\n3")

            registrar = st.form_submit_button("Registrar Ingreso Cocina")

            if registrar:
                try:
                    nombres_list = nombres.strip().splitlines()
                    precios_list = [float(p) for p in precios.strip().splitlines()]
                    cantidades_list = [int(c) for c in cantidades.strip().splitlines()]

                    if len(nombres_list) != len(precios_list) or len(precios_list) != len(cantidades_list):
                        st.error("❌ Las listas deben tener la misma cantidad de líneas.")
                    else:
                        total = 0
                        detalle = []
                        for i in range(len(nombres_list)):
                            sub = precios_list[i] * cantidades_list[i]
                            total += sub
                            detalle.append(f"{cantidades_list[i]} x {nombres_list[i]} (₡{precios_list[i]:,.0f}) = ₡{sub:,.0f}")
                        obs = "\n".join(detalle)
                        insertar_ingreso(fecha, "Cocina", total, obs)
                        st.success(f"✅ Cocina registrada por ₡{total:,.0f}")
                        st.rerun()
                except:
                    st.error("❌ Verifica que precios y cantidades sean válidos.")

    # ====================
    # CRUD INGRESOS
    # ====================
    st.markdown("---")
    st.subheader("🧾 Ingresos registrados")
    ingresos = obtener_ingresos()

    if ingresos:
        df = pd.DataFrame(ingresos, columns=["ID", "Fecha", "Concepto", "Monto", "Observación"])
        st.dataframe(df, use_container_width=True)

        st.markdown("### ✏️ Editar / Eliminar ingreso")
        ingreso_ids = [str(i[0]) for i in ingresos]
        selected_id = st.selectbox("Selecciona el ID del ingreso", ingreso_ids)

        row = next(i for i in ingresos if str(i[0]) == selected_id)
        with st.form("edit_ingreso"):
            col1, col2 = st.columns(2)
            with col1:
                fecha_edit = st.date_input("Fecha", value=pd.to_datetime(row[1], dayfirst=True).date())
                st.markdown(f"📅 Fecha seleccionada: **{fecha_edit.strftime('%d/%m/%Y')}**")
                concepto_edit = st.selectbox("Concepto", ["Diezmo", "Ofrenda", "Cocina", "Otro"], index=["Diezmo", "Ofrenda", "Cocina", "Otro"].index(row[2]))
                monto_edit = st.number_input("Monto", value=row[3], min_value=0.0, format="%.2f", key="edit_monto")
            with col2:
                observacion_edit = st.text_area("Observación", value=row[4], key="edit_obs")

            col3, col4 = st.columns(2)
            actualizar = col3.form_submit_button("💾 Actualizar")
            eliminar = col4.form_submit_button("🗑️ Eliminar")

            if actualizar:
                actualizar_ingreso(row[0], fecha_edit, concepto_edit, monto_edit, observacion_edit)
                st.success("✅ Ingreso actualizado correctamente.")
                st.rerun()

            if eliminar:
                eliminar_ingreso(row[0])
                st.warning("🗑️ Ingreso eliminado.")
                st.rerun()
    else:
        st.info("No hay ingresos registrados aún.")
