from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_fill_color(230, 240, 255)  # azul suave
        self.set_text_color(0, 70, 130)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, '📄 INFORME FINANCIERO', ln=True, align='C', fill=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

    def add_legend(self, inicio, fin):
        self.set_text_color(0)
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 8, f"Este informe fue solicitado por los pastores Jeannett Loaiciga Segura y Carlos Castro Campos.\nPeríodo: {inicio.strftime('%d/%m/%Y')} al {fin.strftime('%d/%m/%Y')}")
        self.ln(5)

    def add_table(self, title, data):
        if not data:
            return
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(255, 200, 120)  # naranja claro
        self.set_text_color(0)
        self.cell(0, 10, title, ln=True, fill=True)
        self.set_font('Arial', '', 10)

        col_widths = [20, 30, 50, 30, 60]
        headers = list(data[0].keys())
        self.set_fill_color(230)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, h, 1, 0, 'C', fill=True)
        self.ln()
        for row in data:
            for i, key in enumerate(headers):
                valor = str(row[key]) if row[key] is not None else ''
                self.cell(col_widths[i], 8, valor, 1)
            self.ln()
        self.ln(5)

    def add_summary(self, ingresos_total, gastos_total):
        balance = ingresos_total - gastos_total
        color = (0, 150, 0) if balance >= 0 else (200, 0, 0)

        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 70, 130)
        self.cell(0, 10, "Resumen del período", ln=True)

        self.set_font('Arial', '', 11)
        self.set_text_color(0)
        self.cell(0, 8, f"Total de ingresos: ₡{ingresos_total:,.2f}", ln=True)
        self.cell(0, 8, f"Total de gastos: ₡{gastos_total:,.2f}", ln=True)
        self.set_text_color(*color)
        self.cell(0, 8, f"Balance final: ₡{balance:,.2f}", ln=True)



