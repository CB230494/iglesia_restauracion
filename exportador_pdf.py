from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Encabezado del PDF
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 51, 102)  # Azul oscuro
        self.cell(0, 10, "Informe Financiero", ln=True, align="C")
        self.ln(5)

    def footer(self):
        # Pie de página
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Página {self.page_no()}', align="C")

    def add_legend(self, fecha_inicio, fecha_fin):
        # Leyenda solicitada al principio del PDF
        self.set_text_color(255, 102, 0)  # Naranja
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 8, f"Este informe fue solicitado por los pastores Jeannett Loaiciga Segura y Carlos Castro Campos.\nPeríodo del informe: {fecha_inicio} al {fecha_fin}", align="L")
        self.ln(5)

    def add_section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(0)
        self.cell(0, 8, title, ln=True)
        self.ln(2)

    def add_table(self, df):
        self.set_font("Helvetica", "", 10)
        self.set_fill_color(200, 220, 255)
        col_widths = [40, 80, 30]  # Ajusta según columnas

        # Encabezado
        for i, col in enumerate(df.columns):
            self.cell(col_widths[i], 8, str(col), border=1, fill=True)
        self.ln()

        # Filas
        for _, row in df.iterrows():
            for i, col in enumerate(df.columns):
                texto = str(row[col])
                # Elimina símbolos no soportados
                texto = texto.encode('latin-1', 'ignore').decode('latin-1')
                self.cell(col_widths[i], 8, texto, border=1)
            self.ln()

        self.ln(5)



