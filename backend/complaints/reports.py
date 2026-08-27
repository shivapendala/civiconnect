import csv
import io
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .models import Complaint

def generate_csv_report(queryset):
    """
    Generates a CSV report from a Complaint queryset.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Category', 'Priority', 'Status', 'Created At', 'Citizen'])

    for c in queryset:
        writer.writerow([
            c.id, 
            c.category.name if c.category else 'N/A', 
            c.priority, 
            c.status, 
            c.created_at.strftime("%Y-%m-%d %H:%M"),
            c.citizen.user.email if c.citizen and c.citizen.user else 'N/A'
        ])
    return output.getvalue()

def generate_excel_report(queryset):
    """
    Generates an Excel (XLSX) report from a Complaint queryset.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Complaints Report"
    
    # Headers
    headers = ['ID', 'Category', 'Priority', 'Status', 'Created At', 'Citizen']
    ws.append(headers)

    for c in queryset:
        ws.append([
            c.id, 
            c.category.name if c.category else 'N/A', 
            c.priority, 
            c.status, 
            c.created_at.strftime("%Y-%m-%d %H:%M"),
            c.citizen.user.email if c.citizen and c.citizen.user else 'N/A'
        ])
    
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.read()

def generate_pdf_report(queryset, title="Complaint Report"):
    """
    Generates a PDF report from a Complaint queryset using ReportLab.
    """
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph(title, styles['Title']))
    elements.append(Spacer(1, 12))
    
    data = [['ID', 'Category', 'Priority', 'Status', 'Created Date']]
    for c in queryset:
        data.append([
            str(c.id),
            c.category.name if c.category else 'N/A',
            c.priority,
            c.status,
            c.created_at.strftime("%Y-%m-%d")
        ])
        
    t = Table(data, colWidths=[50, 120, 80, 100, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    
    elements.append(t)
    doc.build(elements)
    
    output.seek(0)
    return output.read()
