import streamlit as st
import pandas as pd
from datetime import date
from scripts.db_ingresos import (
    init_tables,
    insertar_ingreso,
    obtener_ingresos,
    actualizar_ingreso,
    eliminar_ingreso,
    insertar_gasto,
    obtener_gastos,
    actualizar_gasto,
    eliminar_gasto
)
from scripts.exportador_pdf import PDFReporte

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
        with st.form("form_ingreso_normal", clear_on_submit=True):
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
                    st.success(f"✅ Ingreso registrado correctamente como {concepto}.")
                    st.rerun()
                else:
                    st.error("❌ El monto debe ser mayor a 0.")

    # ====================
    # INGRESO COCINA (CAJA)
    # ====================
    else:
        st.markdown("### 🍽️ Cocina - Caja registradora")
        with st.form("form_cocina", clear_on_submit=True):
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
                nombres_list = nombres.strip().splitlines()
                precios_list = [float(p) for p in precios.strip().splitlines()]
                cantidades_list = [int(c) for c in cantidades.strip().splitlines()]

                if len(nombres_list) != len(precios_list) or len(precios_list) != len(cantidades_list):
                    pass  # Silenciado
                else:
                    total = 0
                    detalle = []
                    for i in range(len(nombres_list)):
                        sub = precios_list[i] * cantidades_list[i]
                        total += sub
                        detalle.append(f"{cantidades_list[i]} x {nombres_list[i]} (₡{precios_list[i]:,.0f}) = ₡{sub:,.0f}")
                    obs = "\n".join(detalle)
                    insertar_ingreso(fecha, "Cocina", total, obs)
                    st.success(f"✅ Ingreso registrado: Cocina por ₡{total:,.0f} (ej. almuerzo agregado)")
                    st.rerun()

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


# =====================================
# 💸 GASTOS - IGLESIA RESTAURACIÓN COLONIA CARVAJAL
# =====================================
elif opcion == "💸 Gastos":
    st.title("💸 Registro de Gastos - Iglesia Restauración Colonia Carvajal")

    st.markdown("### ➕ Nuevo gasto")
    with st.form("form_gasto", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha del gasto", value=date.today())
            st.markdown(f"📅 Fecha seleccionada: **{fecha.strftime('%d/%m/%Y')}**")
            motivo = st.text_input("Motivo")
        with col2:
            monto = st.number_input("Monto (₡)", min_value=0.0, format="%.2f")
            observacion = st.text_area("Observación (opcional)")

        enviar = st.form_submit_button("Registrar Gasto")

        if enviar:
            if motivo and monto > 0:
                insertar_gasto(fecha, motivo, monto, observacion)
                st.success(f"✅ Gasto registrado correctamente: {motivo} por ₡{monto:,.2f}")
                st.rerun()
            else:
                st.error("❌ Todos los campos obligatorios deben estar completos.")

    st.markdown("---")
    st.subheader("🧾 Gastos registrados")
    gastos = obtener_gastos()

    if gastos:
        df = pd.DataFrame(gastos, columns=["ID", "Fecha", "Motivo", "Monto", "Observación"])
        st.dataframe(df, use_container_width=True)

        st.markdown("### ✏️ Editar / Eliminar gasto")
        gasto_ids = [str(g[0]) for g in gastos]
        selected_id = st.selectbox("Selecciona el ID del gasto", gasto_ids)

        row = next(g for g in gastos if str(g[0]) == selected_id)
        with st.form("edit_gasto"):
            col1, col2 = st.columns(2)
            with col1:
                fecha_edit = st.date_input("Fecha", value=pd.to_datetime(row[1], dayfirst=True).date())
                st.markdown(f"📅 Fecha seleccionada: **{fecha_edit.strftime('%d/%m/%Y')}**")
                motivo_edit = st.text_input("Motivo", value=row[2])
            with col2:
                monto_edit = st.number_input("Monto", value=row[3], min_value=0.0, format="%.2f", key="edit_monto_gasto")
                observacion_edit = st.text_area("Observación", value=row[4], key="edit_obs_gasto")

            col3, col4 = st.columns(2)
            actualizar = col3.form_submit_button("💾 Actualizar")
            eliminar = col4.form_submit_button("🗑️ Eliminar")

            if actualizar:
                actualizar_gasto(row[0], fecha_edit, motivo_edit, monto_edit, observacion_edit)
                st.success("✅ Gasto actualizado correctamente.")
                st.rerun()

            if eliminar:
                eliminar_gasto(row[0])
                st.warning("🗑️ Gasto eliminado.")
                st.rerun()
    else:
        st.info("No hay gastos registrados aún.")

# =====================================
# 📊 REPORTES - IGLESIA RESTAURACIÓN COLONIA CARVAJAL
# =====================================
elif opcion == "📊 Reportes":
    st.title("📊 Reporte financiero - Iglesia Restauración Colonia Carvajal")

    st.markdown("### Seleccione el rango de fechas")
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Fecha inicial", value=date.today())
    with col2:
        fecha_final = st.date_input("Fecha final", value=date.today())

    if fecha_inicio > fecha_final:
        st.error("❌ La fecha inicial no puede ser posterior a la fecha final.")
    else:
        ingresos_filtrados = [
            i for i in obtener_ingresos()
            if fecha_inicio <= pd.to_datetime(i[1], dayfirst=True).date() <= fecha_final
        ]

        gastos_filtrados = [
            g for g in obtener_gastos()
            if fecha_inicio <= pd.to_datetime(g[1], dayfirst=True).date() <= fecha_final
        ]

        total_ingresos = sum(i[3] for i in ingresos_filtrados)
        total_gastos = sum(g[3] for g in gastos_filtrados)
        balance = total_ingresos - total_gastos

        st.markdown("### 📋 Resumen financiero")
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total de ingresos", f"₡{total_ingresos:,.2f}")
        col2.metric("💸 Total de gastos", f"₡{total_gastos:,.2f}")

        if balance >= 0:
            col3.metric("📈 Balance", f"₡{balance:,.2f}", delta="Ganancia", delta_color="normal")
        else:
            col3.metric("📉 Balance", f"₡{balance:,.2f}", delta="Pérdida", delta_color="inverse")

        with st.expander("📥 Ver detalle de ingresos"):
            if ingresos_filtrados:
                df_i = pd.DataFrame(ingresos_filtrados, columns=["ID", "Fecha", "Concepto", "Monto", "Observación"])
                st.dataframe(df_i, use_container_width=True)
            else:
                st.info("No hay ingresos en este rango.")

        with st.expander("💸 Ver detalle de gastos"):
            if gastos_filtrados:
                df_g = pd.DataFrame(gastos_filtrados, columns=["ID", "Fecha", "Motivo", "Monto", "Observación"])
                st.dataframe(df_g, use_container_width=True)
            else:
                st.info("No hay gastos en este rango.")

        # =====================
        # 📄 Exportar informe en PDF
        # =====================
        if ingresos_filtrados or gastos_filtrados:
            st.markdown("### 📄 Exportar informe")
            if st.button("📄 Exportar informe en PDF"):
                pdf = PDFReporte()
                pdf.add_page()
                pdf.add_leyenda(fecha_inicio, fecha_final)
                pdf.add_cuadro_resumen(total_ingresos, total_gastos, balance)

                # Agrupar ingresos por concepto
                if ingresos_filtrados:
                    resumen = {}
                    for i in ingresos_filtrados:
                        concepto = i[2]
                        resumen[concepto] = resumen.get(concepto, 0) + i[3]

                    columnas_i = ["Concepto", "Total"]
                    datos_i = [[k, f"{v:,.2f}"] for k, v in resumen.items()]
                    pdf.add_tabla_detalle("Ingresos por concepto", datos_i, columnas_i)

                # Detalle de gastos
                if gastos_filtrados:
                    columnas_g = ["Fecha", "Motivo", "Monto"]
                    datos_g = [[g[1], g[2], f"{g[3]:,.2f}"] for g in gastos_filtrados]
                    pdf.add_tabla_detalle("Gastos registrados", datos_g, columnas_g)

                # Generar PDF seguro
                pdf_bytes = pdf.output(dest="S").encode("latin-1", errors="replace")
                st.download_button(
                    "⬇️ Descargar PDF",
                    data=pdf_bytes,
                    file_name="informe_financiero.pdf",
                    mime="application/pdf"
                )


