from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    Flowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "DOCUMENTO_ENTREGA.pdf"


class RelationshipDiagram(Flowable):
    def __init__(self, width=16 * cm, height=10 * cm):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        canvas = self.canv
        box_width = 4.2 * cm
        box_height = 1.4 * cm
        positions = {
            "FUENTES": (0.4 * cm, 7.7 * cm),
            "PRODUCTOS": (5.9 * cm, 7.7 * cm),
            "TECNOLOGIA": (2.0 * cm, 3.8 * cm),
            "LIBROS": (8.7 * cm, 3.8 * cm),
            "CATEGORIAS": (8.7 * cm, 0.5 * cm),
        }

        def center(name):
            x, y = positions[name]
            return x + box_width / 2, y + box_height / 2

        canvas.setStrokeColor(colors.HexColor("#2563eb"))
        canvas.setFillColor(colors.HexColor("#eff6ff"))
        canvas.setLineWidth(1.2)
        for name, (x, y) in positions.items():
            canvas.roundRect(x, y, box_width, box_height, 5, fill=1, stroke=1)
            canvas.setFillColor(colors.HexColor("#1e3a8a"))
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawCentredString(x + box_width / 2, y + box_height / 2 - 3, name)
            canvas.setFillColor(colors.HexColor("#eff6ff"))

        for source, target in (("FUENTES", "PRODUCTOS"), ("PRODUCTOS", "TECNOLOGIA"), ("PRODUCTOS", "LIBROS"), ("LIBROS", "CATEGORIAS")):
            x1, y1 = center(source)
            x2, y2 = center(target)
            canvas.setStrokeColor(colors.HexColor("#64748b"))
            canvas.line(x1, y1, x2, y2)


def build_pdf():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#1e3a8a"), spaceAfter=18))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=9, leading=12))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], textColor=colors.HexColor("#1e3a8a"), spaceBefore=12, spaceAfter=8))
    document = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=1.7 * cm, leftMargin=1.7 * cm, topMargin=1.5 * cm, bottomMargin=1.5 * cm)
    story = []

    story.append(Paragraph("Laboratorio ETL con Scrapy y SQLite", styles["TitleCenter"]))
    story.append(Paragraph("Extraccion, transformacion, almacenamiento y consulta de datos", styles["Normal"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("1. Objetivo", styles["Section"]))
    story.append(Paragraph("Construir un proceso ETL que extraiga informacion de libros y productos tecnologicos, transforme los datos y los almacene en una base de datos SQLite relacional para realizar consultas analiticas.", styles["BodyText"]))

    story.append(Paragraph("2. Fuentes exploradas", styles["Section"]))
    sources = [
        ["Fuente", "Informacion", "Registros"],
        ["Books to Scrape", "Libros, precio, calificacion, categoria, disponibilidad y descripcion.", "1.000 libros"],
        ["Web Scraper Test Sites", "Laptops, precio, calificacion, categoria y descripcion.", "117 productos"],
    ]
    table = Table(sources, colWidths=[4 * cm, 9 * cm, 3 * cm])
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("FONTSIZE", (0, 0), (-1, -1), 8)]))
    story.append(table)
    story.append(Paragraph("La informacion comun entre ambas fuentes es nombre, precio, calificacion y URL. Categoria, descripcion y disponibilidad dependen de cada sitio.", styles["Small"]))

    story.append(Paragraph("3. Extraccion y transformacion", styles["Section"]))
    story.append(Paragraph("Los spiders BooksSpider y LaptopsSpider recorren las paginas disponibles y guardan los resultados en archivos JSON. La transformacion elimina espacios innecesarios, convierte precios y calificaciones a tipos numericos, normaliza disponibilidad, identifica valores faltantes y elimina duplicados por fuente y URL.", styles["BodyText"]))

    story.append(Paragraph("4. Modelo de base de datos", styles["Section"]))
    story.append(RelationshipDiagram())
    story.append(Paragraph("Fuentes se relaciona con productos. Productos contiene los atributos comunes y se especializa en tecnologia o libros. Libros se relaciona con categorias.", styles["Small"]))

    story.append(PageBreak())
    story.append(Paragraph("5. Consultas SQL y resultados", styles["Section"]))
    results = [
        ["Consulta", "Resultado"],
        ["1. Producto junto con fuente", "Relaciona productos con fuentes mediante id_fuente."],
        ["2. Informacion de categorias", "Relaciona libros, productos y categorias mediante claves foraneas."],
        ["3. Productos por tipo", "libro: 1.000; tecnologia: 117."],
        ["4. Producto mas costoso", "Asus ROG Strix SCAR Edition GL503VM-ED115T: 1799.00."],
        ["5. Producto mas economico", "An Abundance of Katherines: 10.00."],
        ["6. Precio promedio", "126.65."],
        ["7. Calificacion promedio", "2.86."],
        ["8. Fuente con mas productos", "Books to Scrape: 1.000 productos."],
    ]
    result_table = Table(results, colWidths=[5 * cm, 11 * cm])
    result_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("FONTSIZE", (0, 0), (-1, -1), 8)]))
    story.append(result_table)

    story.append(Paragraph("6. Validacion", styles["Section"]))
    validation = [
        ["Indicador", "Resultado"],
        ["Productos totales", "1.117"],
        ["Registros en libros", "1.000"],
        ["Registros en tecnologia", "117"],
        ["URLs duplicadas", "0"],
        ["Productos sin nombre o URL", "0"],
        ["Errores de claves foraneas", "0"],
    ]
    validation_table = Table(validation, colWidths=[9 * cm, 7 * cm])
    validation_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("FONTSIZE", (0, 0), (-1, -1), 8)]))
    story.append(validation_table)
    story.append(Spacer(1, 12))
    story.append(Paragraph("Archivos principales: etl/spiders.py, etl/transform.py, etl/database.py, etl/schema.sql, etl/queries.sql, etl/run.py y etl.db.", styles["Small"]))
    document.build(story)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT)
