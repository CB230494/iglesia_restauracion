from fpdf import FPDF
import pandas as pd
from datetime import datetime, date

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.set_text_color(33, 37, 41)  # Azul oscuro
        self.cell(0, 10, "Informe Financiero - Iglesia Restauración", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def add_title(self, texto):
        self.set_font("Arial", "B", 16)
        self.set_text_color(33, 37, 41)
        self.cell(0, 10, texto, ln=True, align="L")
        self.ln(5)

    def add_subtitle(self, texto):
        self.set_font("Arial", "B", 12)
        self.set_text_color(255, 87, 34)  # Naranja
        self.cell(0, 10, texto, ln=True, align="L")

    def add_paragraph(self, texto):
        self.set_font("Arial", "", 11)
        self.set_text_color(33, 33, 33)
        self.multi_cell(0, 10, texto)
        self.ln(3)

    def add_table(self, df, title, emoji=""):
        self.set_font("Arial", "B", 13)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, f"{emoji} {title}", ln=True)
        self.set_font("Arial", "B", 10)
        self.set_text_color(0, 0, 0)

        col_widths = [10, 30, 50, 30, 70]
        headers = ["id", "fecha", "concepto", "monto", "observacion"]
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1)
        self.ln()

        self.set_font("Arial", "", 10)
        for _, row in df.iterrows():
            self.cell(col_widths[0], 8, str(row["id"]), 1)

            # Manejar fecha correctamente
            fecha_str = row["fecha"].strftime('%d/%m/%Y') if isinstance(row["fecha"], (datetime, date)) else str(row["fecha"])
            self.cell(col_widths[1], 8, fecha_str, 1)

            self.cell(col_widths[2], 8, str(row["concepto"]), 1)
            self.cell(col_widths[3], 8, str(row["monto"]), 1)

            observacion = "" if pd.isna(row["observacion"]) or str(row["observacion"]).lower() == "none" else str(row["observacion"])
            self.cell(col_widths[4], 8, observacion, 1)

            self.ln()
        self.ln(5)

    def generate_report(self, ingresos_df, gastos_df, fecha_inicio, fecha_fin):
        self.add_page()

        # Leyenda principal
        self.set_font("Arial", "", 11)
        leyenda = (
            "Este informe fue solicitado por los pastores Jeannett Loaiciga Segura "
            "y Carlos Castro Campos.\n\n"
            f"Período del informe: {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}\n"
        )
        self.multi_cell(0, 10, leyenda)
        self.ln(3)

        # Títulos
        self.add_title("Exportar PDF del Informe Financiero")
        self.add_paragraph("A continuación se presenta el resumen financiero correspondiente al periodo seleccionado.")

        if not ingresos_df.empty:
            self.add_table(ingresos_df, "Ingresos en el período", emoji="💰")
        else:
            self.add_paragraph("No se registraron ingresos durante el período seleccionado.")

        if not gastos_df.empty:
            self.add_table(gastos_df, "Gastos en el período", emoji="💸")
        else:
            self.add_paragraph("No se registraron gastos durante el período seleccionado.")


