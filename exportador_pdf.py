from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Título del documento
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 51, 102)  # Azul oscuro
        self.cell(0, 10, "Informe Financiero - Iglesia Restauración", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def generate_report(self, ingresos, gastos, fecha_inicio, fecha_fin):
        self.add_page()
        self.set_auto_page_break(auto=True, margin=15)

        # Leyenda solicitada
        self.set_font("Helvetica", "", 12)
        self.set_text_color(0)
        leyenda = (
            "Este informe fue solicitado por los pastores Jeannett Loaiciga Segura "
            "y Carlos Castro Campos"
        )
        self.multi_cell(0, 10, leyenda)
        self.ln(4)

        # Período del informe
        periodo = f"Período del informe: {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}"
        self.set_text_color(255, 102, 0)  # Naranja
        self.cell(0, 10, periodo, ln=True)
        self.ln(5)

        # --- Ingresos ---
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, "Resumen de Ingresos", ln=True)
        self.ln(2)

        if ingresos.empty:
            self.set_font("Helvetica", "", 12)
            self.set_text_color(0)
            self.cell(0, 10, "No hay ingresos registrados en este período.", ln=True)
        else:
            self.set_font("Helvetica", "B", 11)
            self.set_fill_color(0, 51, 102)
            self.set_text_color(255)
            self.cell(60, 8, "Fecha", 1, 0, "C", True)
            self.cell(80, 8, "Tipo", 1, 0, "C", True)
            self.cell(40, 8, "Monto (₡)", 1, 1, "C", True)

            self.set_font("Helvetica", "", 11)
            self.set_text_color(0)
            total_ingresos = 0
            for _, row in ingresos.iterrows():
                self.cell(60, 8, row["fecha"].strftime("%d/%m/%Y"), 1)
                self.cell(80, 8, row["tipo"], 1)
                self.cell(40, 8, f"₡{row['monto']:,.0f}", 1, ln=True)
                total_ingresos += row["monto"]

            self.set_font("Helvetica", "B", 12)
            self.cell(140, 10, "Total de Ingresos", 1)
            self.cell(40, 10, f"₡{total_ingresos:,.0f}", 1, ln=True)

        self.ln(10)

        # --- Gastos ---
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, "Resumen de Gastos", ln=True)
        self.ln(2)

        if gastos.empty:
            self.set_font("Helvetica", "", 12)
            self.set_text_color(0)
            self.cell(0, 10, "No hay gastos registrados en este período.", ln=True)
        else:
            self.set_font("Helvetica", "B", 11)
            self.set_fill_color(255, 102, 0)
            self.set_text_color(255)
            self.cell(60, 8, "Fecha", 1, 0, "C", True)
            self.cell(80, 8, "Categoría", 1, 0, "C", True)
            self.cell(40, 8, "Monto (₡)", 1, 1, "C", True)

            self.set_font("Helvetica", "", 11)
            self.set_text_color(0)
            total_gastos = 0
            for _, row in gastos.iterrows():
                self.cell(60, 8, row["fecha"].strftime("%d/%m/%Y"), 1)
                self.cell(80, 8, row["categoria"], 1)
                self.cell(40, 8, f"₡{row['monto']:,.0f}", 1, ln=True)
                total_gastos += row["monto"]

            self.set_font("Helvetica", "B", 12)
            self.cell(140, 10, "Total de Gastos", 1)
            self.cell(40, 10, f"₡{total_gastos:,.0f}", 1, ln=True)

        self.ln(10)

        # Saldo final
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(0, 102, 0)
        saldo = total_ingresos - total_gastos
        self.cell(140, 12, "Saldo Final del Período", 1)
        self.cell(40, 12, f"₡{saldo:,.0f}", 1, ln=True)

        self.output("informe_financiero.pdf", "F")


