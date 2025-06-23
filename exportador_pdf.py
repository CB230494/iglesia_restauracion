from fpdf import FPDF
import re

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(255, 255, 255)  # Blanco
        self.set_fill_color(0, 102, 204)    # Azul
        self.cell(0, 10, "INFORME FINANCIERO - IGLESIA RESTAURACIÓN", 0, 1, 'C', fill=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def limpiar_texto(self, texto):
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
            u"\U00002700-\U000027BF"
            u"\U0001F900-\U0001F9FF"
            "]+", flags=re.UNICODE)
        texto_limpio = emoji_pattern.sub(r'', str(texto))
        return texto_limpio.encode("latin-1", "ignore").decode("latin-1")

    def add_legend(self, fecha_inicio, fecha_fin):
        self.set_font('Arial', '', 11)
        self.set_text_color(0)
        self.set_fill_color(255, 153, 51)  # Naranja
        self.cell(0, 10, "Este informe fue solicitado por los pastores Jeannett Loaiciga Segura y Carlos Castro Campos", 0, 1, 'L', fill=True)
        self.cell(0, 10, f"Período del informe: {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}", 0, 1, 'L')
        self.ln(5)

    def add_table(self, titulo, data):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, self.limpiar_texto(titulo), 0, 1)

        if not data:
            self.set_font('Arial', '', 10)
            self.set_text_color(150)
            self.cell(0, 10, "No hay registros disponibles.", 0, 1)
            return

        columnas = list(data[0].keys())
        self.set_font('Arial', 'B', 10)
        self.set_text_color(0)
        for col in columnas:
            self.cell(40, 8, self.limpiar_texto(col), 1)
        self.ln()

        self.set_font('Arial', '', 10)
        for row in data:
            for col in columnas:
                valor = self.limpiar_texto(row[col])
                self.cell(40, 8, valor, 1)
            self.ln()
        self.ln(5)

    def add_summary(self, total_ingresos, total_gastos):
        balance = total_ingresos - total_gastos
        color = (0, 153, 0) if balance >= 0 else (204, 0, 0)

        self.set_font('Arial', 'B', 11)
        self.set_text_color(0)
        self.cell(0, 10, "Resumen Financiero:", 0, 1)

        self.set_font('Arial', '', 10)
        self.cell(0, 8, f"Total Ingresos: ₡{total_ingresos:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 0, 1)
        self.cell(0, 8, f"Total Gastos: ₡{total_gastos:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 0, 1)

        self.set_text_color(*color)
        self.cell(0, 8, f"Balance Final: ₡{balance:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 0, 1)



