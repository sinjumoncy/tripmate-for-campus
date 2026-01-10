from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_budget_pdf(filename, content_text):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    for line in content_text.split("\n"):
        elements.append(Paragraph(line.replace("&", "&amp;"), styles["Normal"]))
        elements.append(Spacer(1, 8))

    doc.build(elements)