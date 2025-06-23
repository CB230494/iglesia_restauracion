from fpdf import FPDF
import datetime

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 102, 204)  # Azul
        self.cell(0, 10, "Informe Financiero - Iglesia Restauración", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128)
        page = "Página %s" % self.page_no()
        self.cell(0, 10, page, align="C")

    def add_legend(self, nombre_pastores, fecha_inicio, fecha_fin):
        self.set_font("Arial", "", 12)
        self.set_text_color(0)
        texto = f"Este informe fue solicitado por los pastores {nombre_pastores}. "
        texto += f"Corresponde al periodo del {fecha_inicio} al {fecha_fin}."
        self.multi_cell(0, 10, texto)
        self.ln(5)

    def add_table(self, title, data):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(255, 102, 0)  # Naranja
        self.set_text_color(255)
        self.cell(0, 10, title, ln=True, fill=True)
        self.set_text_color(0)

        if not data.empty:
            self.set_font("Arial", "B", 10)
            for col in data.columns:
                self.cell(40, 8, str(col), border=1)
            self.ln()

            self.set_font("Arial", "", 10)
            for _, row in data.iterrows():
                for item in row:
                    self.cell(40, 8, str(item), border=1)
                self.ln()
        else:
            self.set_font("Arial", "I", 10)
            self.cell(0, 10, "No hay datos disponibles.", ln=True)
        self.ln(5)



