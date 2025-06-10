import streamlit as st
from scripts.db_ingresos import (
    init_tables,
    insertar_ingreso,
    insertar_gasto
)

# Inicializar la base de datos y las tablas si no existen
init_tables()

# Menú lateral
st.sidebar.title("📌 Navegación")
opcion = st.sidebar.radio("Ir a:", ["📥 Ingresos", "💸 Gastos", "📊 Reportes (próximamente)"])

# ==========================
# 📥 REGISTRO DE INGRESOS
# ==========================
if opcion == "📥 Ingresos":
    st.title("📥 Registro de Ingresos - Iglesia Restauración")

    concepto = st.selectbox("Concepto", ["Diezmo", "Ofrenda", "Cocina", "Otro"])

    if concepto != "Cocina":
        # Ingreso tradicional
        with st.form("form_ingreso_normal"):
            monto = st.number_input("Monto (₡)", min_value=0.0, format="%.2f")
            observacion = st.text_area("Observación (opcional)")
            enviar = st.form_submit_button("Registrar Ingreso")

            if enviar:
                if monto > 0:
                    insertar_ingreso(concepto, monto, observacion)
                    st.success("✅ Ingreso registrado correctamente.")
                else:
                    st.error("❌ El monto debe ser mayor a 0.")
    else:
        # Modo caja registradora (cocina)
        st.subheader("🍽️ Registrar ventas de Cocina")

        with st.form("form_cocina"):
            productos = []
            total = 0
            col1, col2, col3 = st.columns([4, 2, 2])

            with col1:
                nombres = st.text_area("Productos vendidos (uno por línea)", placeholder="Ej: Refresco\nEmpanada\nQueque")

            with col2:
                precios = st.text_area("Precios unitarios (₡)", placeholder="Ej: 500\n700\n1200")

            with col3:
                cantidades = st.text_area("Cantidades", placeholder="Ej: 2\n3\n1")

            registrar = st.form_submit_button("Registrar Ingreso Cocina")

            if registrar:
                try:
                    nombres_list = nombres.strip().splitlines()
                    precios_list = [float(p) for p in precios.strip().splitlines()]
                    cantidades_list = [int(c) for c in cantidades.strip().splitlines()]

                    if not (len(nombres_list) == len(precios_list) == len(cantidades_list)):
                        st.error("❌ Todos los campos deben tener la misma cantidad de líneas.")
                    else:
                        detalles = []
                        total = 0
                        for i in range(len(nombres_list)):
                            subtotal = precios_list[i] * cantidades_list[i]
                            total += subtotal
                            detalles.append(f"{cantidades_list[i]} x {nombres_list[i]} (₡{precios_list[i]:,.0f}) = ₡{subtotal:,.0f}")

                        observacion = "\n".join(detalles)
                        insertar_ingreso("Cocina", total, observacion)
                        st.success(f"✅ Ingreso por Cocina registrado por un total de ₡{total:,.0f}")
                except:
                    st.error("❌ Verifica que los precios sean números (ej: 500) y las cantidades enteros (ej: 2)")

# ==========================
# 💸 REGISTRO DE GASTOS
# ==========================
elif opcion == "💸 Gastos":
    st.title("💸 Registro de Gastos - Iglesia Restauración")

    with st.form("form_gasto"):
        motivo = st.text_input("Motivo del gasto")
        monto = st.number_input("Monto (₡)", min_value=0.0, format="%.2f", key="gasto_monto")
        observacion = st.text_area("Observación (opcional)", key="gasto_obs")
        enviar = st.form_submit_button("Registrar Gasto")

        if enviar:
            if motivo and monto > 0:
                insertar_gasto(motivo, monto, observacion)
                st.success("✅ Gasto registrado correctamente.")
            else:
                st.error("❌ Por favor, complete todos los campos obligatorios.")

# ==========================
# 📊 REPORTES (EN CONSTRUCCIÓN)
# ==========================
elif opcion == "📊 Reportes (próximamente)":
    st.title("📊 Reportes - En construcción...")
    st.info("Muy pronto podrás visualizar ingresos y gastos por fecha, ver gráficos y exportar a PDF.")

