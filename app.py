import streamlit as st
from scripts.db_ingresos import init_ingresos_table, insertar_ingreso
from scripts.db_gastos import init_gastos_table, insertar_gasto

# Inicializar las tablas si no existen
init_ingresos_table()
init_gastos_table()

# Menú lateral
st.sidebar.title("📌 Navegación")
opcion = st.sidebar.radio("Ir a:", ["📥 Ingresos", "💸 Gastos", "📊 Reportes (próximamente)"])

# Pantalla: INGRESOS
if opcion == "📥 Ingresos":
    st.title("📥 Registro de Ingresos - Iglesia Restauración")

    with st.form("form_ingreso"):
        concepto = st.selectbox("Concepto", ["Diezmo", "Ofrenda", "Cocina", "Otro"])
        monto = st.number_input("Monto (₡)", min_value=0.0, format="%.2f")
        observacion = st.text_area("Observación (opcional)")
        enviar = st.form_submit_button("Registrar Ingreso")

        if enviar:
            if monto > 0 and concepto:
                insertar_ingreso(concepto, monto, observacion)
                st.success("✅ Ingreso registrado correctamente.")
            else:
                st.error("❌ Por favor, complete todos los campos obligatorios.")

# Pantalla: GASTOS
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

# Pantalla: REPORTES (vacía por ahora)
elif opcion == "📊 Reportes (próximamente)":
    st.title("📊 Reportes - En construcción...")
    st.info("Muy pronto podrás visualizar ingresos y gastos por fecha, gráficos y exportar a PDF.")
