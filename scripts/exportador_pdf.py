from fpdf import FPDF
from datetime import datetime

class PDFReporte(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, "📊 Informe Financiero - Iglesia Restauración Colonia Carvajal", 0, 1, "C")
        self.ln(5)

    def add_leyenda(self, fecha_inicio, fecha_final):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(50, 50, 50)
        self.set_fill_color(230, 230, 250)
        self.multi_cell(0, 8,
            f"Este informe fue solicitado por los pastores Jeannett Loáiciga Segura y Carlos Castro Campos "
            f"para el periodo comprendido entre el {fecha_inicio.strftime('%d/%m/%Y')} y el {fecha_final.strftime('%d/%m/%Y')}.",
            border=1, align="L", fill=True)
        self.ln(3)

        # Introducción adaptada
        dias = (fecha_final - fecha_inicio).days + 1
        if dias <= 1:
            tipo = "diario"
        elif dias <= 7:
            tipo = "semanal"
        elif dias <= 15:
            tipo = "quincenal"
        else:
            tipo = "mensual"

        self.set_font("Helvetica", "I", 10)
        self.multi_cell(0, 7,
            f"Este informe es de carácter {tipo}, con el fin de brindar transparencia en la gestión económica "
            f"de la iglesia durante el periodo seleccionado.",
            border=0)
        self.ln(5)

    def add_cuadro_resumen(self, ingresos, gastos, balance):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(60, 10, "Categoría", 1, 0, "C", True)
        self.cell(60, 10, "Monto (₡)", 1, 1, "C", True)

        self.set_font("Helvetica", "", 11)
        self.cell(60, 10, "Total de ingresos", 1)
        self.cell(60, 10, f"{ingresos:,.2f}", 1, 1)

        self.cell(60, 10, "Total de gastos", 1)
        self.cell(60, 10, f"{gastos:,.2f}", 1, 1)

        if balance >= 0:
            self.set_text_color(0, 128, 0)  # verde
        else:
            self.set_text_color(200, 0, 0)  # rojo

        self.cell(60, 10, "Balance", 1)
        self.cell(60, 10, f"{balance:,.2f}", 1, 1)
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def add_tabla_detalle(self, titulo, data, columnas):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, titulo, 0, 1, "L", False)

        self.set_font("Helvetica", "B", 10)
        for col in columnas:
            self.cell(45, 8, col, 1, 0, "C", True)
        self.ln()

        self.set_font("Helvetica", "", 9)
        for row in data:
            for i, col in enumerate(columnas):
                texto = str(row[i]) if i < len(row) else ""
                self.cell(45, 7, texto[:30], 1)
            self.ln()
        self.ln(4)
