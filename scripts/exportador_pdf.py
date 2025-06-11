from fpdf import FPDF

class PDFReporte(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.set_fill_color(220, 220, 220)
        self.cell(0, 10, "Informe Financiero - Iglesia Restauración Colonia Carvajal", 0, 1, "C", fill=True)
        self.ln(5)

    def add_leyenda(self, fecha_inicio, fecha_final):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, "Este informe ha sido solicitado por los pastores Jeannett Loáiciga Segura y Carlos Castro Campos.")
        self.ln(3)

        dias = (fecha_final - fecha_inicio).days
        if dias == 0:
            tipo = "Informe diario"
        elif dias <= 15:
            tipo = "Informe quincenal"
        else:
            tipo = "Informe mensual"

        self.set_font("Arial", "I", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"{tipo} - Rango: {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_final.strftime('%d/%m/%Y')}", 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def add_cuadro_resumen(self, ingresos, gastos, balance):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(60, 10, "Categoría", 1, 0, "C", True)
        self.cell(60, 10, "Monto (₡)", 1, 1, "C", True)

        self.set_font("Arial", "", 11)
        self.cell(60, 10, "Total de ingresos", 1)
        self.cell(60, 10, f"{ingresos:,.2f}", 1, 1)

        self.cell(60, 10, "Total de gastos", 1)
        self.cell(60, 10, f"{gastos:,.2f}", 1, 1)

        if balance >= 0:
            self.set_text_color(0, 128, 0)
        else:
            self.set_text_color(200, 0, 0)

        self.cell(60, 10, "Balance", 1)
        self.cell(60, 10, f"{balance:,.2f}", 1, 1)
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def add_tabla_detalle(self, titulo, data, columnas):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, titulo, 0, 1, "L")
        self.set_fill_color(240, 240, 240)

        self.set_font("Arial", "B", 10)
        col_width = 190 // len(columnas)
        for col in columnas:
            self.cell(col_width, 8, col, 1, 0, "C", True)
        self.ln()

        self.set_font("Arial", "", 10)
        for row in data:
            for item in row:
                self.cell(col_width, 8, str(item), 1)
            self.ln()
        self.ln(4)


