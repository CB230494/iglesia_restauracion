from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'Informe Financiero - Iglesia Restauración Colonia Carvajal', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Página {self.page_no()} - Sistema de Control Financiero', align='C')

    def add_legend(self, fecha_inicio, fecha_fin):
        self.set_font('Arial', '', 10)
        self.set_text_color(0)
        self.multi_cell(0, 8, f"Este informe fue solicitado por los pastores Jeannett Loaiciga Segura y Carlos Castro Campos\nPeríodo del informe: {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}")
        self.ln(5)

    def add_table(self, titulo, data):
        self.set_font('Arial', 'B', 11)
        self.set_text_color(0)
        self.cell(0, 10, titulo, ln=True)
        self.set_font('Arial', '', 9)

        if not data:
            self.cell(0, 8, "No hay registros disponibles en este período.", ln=True)
            self.ln(5)
            return

        headers = ["Fecha", "Concepto", "Monto", "Observación"]
        col_widths = [30, 50, 30, 80]

        for i, header in enumerate(headers):
            self.set_fill_color(200, 200, 200)
            self.cell(col_widths[i], 8, header, 1, 0, 'C', True)
        self.ln()

        for row in data:
            self.cell(col_widths[0], 8, row["fecha"][:10], 1)
            self.cell(col_widths[1], 8, row["concepto"], 1)
            monto_str = f"CRC {row['monto']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.cell(col_widths[2], 8, monto_str, 1)
            obs = row["observacion"] if row["observacion"] else "—"
            self.cell(col_widths[3], 8, obs[:60], 1)
            self.ln()
        self.ln(5)

    def add_summary(self, total_ingresos, total_gastos):
        balance = total_ingresos - total_gastos
        color = (0, 153, 0) if balance >= 0 else (204, 0, 0)

        self.set_font('Arial', 'B', 11)
        self.set_text_color(0)
        self.cell(0, 10, "Resumen Financiero:", 0, 1)

        self.set_font('Arial', '', 10)
        ingresos_str = f"CRC {total_ingresos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        gastos_str = f"CRC {total_gastos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        balance_str = f"CRC {balance:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        self.cell(0, 8, f"Total Ingresos: {ingresos_str}", 0, 1)
        self.cell(0, 8, f"Total Gastos: {gastos_str}", 0, 1)
        self.set_text_color(*color)
        self.cell(0, 8, f"Balance Final: {balance_str}", 0, 1)



