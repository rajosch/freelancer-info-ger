import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def save_invoice_to_csv(client_name, client_address, freelancer_name, freelancer_address, invoice_id, itemized_data):
    # Define the CSV file name and path
    file_name = f"{invoice_id}_invoice.csv"
    file_path = os.path.join("invoices", file_name)

    # Check if the "invoices" directory exists; if not, create it
    if not os.path.exists("invoices"):
        os.makedirs("invoices")

    # Define the invoice data
    invoice_data = {
        "Client Name": client_name,
        "Client Address": client_address,
        "Freelancer Name": freelancer_name,
        "Freelancer Address": freelancer_address,
        "Invoice ID": invoice_id,
    }

    # Create a list of dictionaries for each item
    item_dicts = []
    for item in itemized_data:
        item_dict = invoice_data.copy()
        item_dict.update({
            "Item": item[0],
            "Price": item[1],
            "Tax": item[2]
        })
        item_dicts.append(item_dict)

    # Create a pandas DataFrame and save it as a CSV file
    df = pd.DataFrame(item_dicts)
    df.to_csv(file_path, index=False)
    

def save_invoice_to_pdf(client_name, client_address, freelancer_name, freelancer_address, invoice_id, itemized_data):
    # Define the PDF file name and path
    file_name = f"{invoice_id}_invoice.pdf"
    file_path = os.path.join("invoices", file_name)

    # Check if the "invoices" directory exists; if not, create it
    if not os.path.exists("invoices"):
        os.makedirs("invoices")

    # Create a SimpleDocTemplate for the PDF
    pdf = SimpleDocTemplate(file_path, pagesize=letter)

    # Define the invoice data as a table
    invoice_data = [
        ["Client Name", client_name],
        ["Client Address", client_address],
        ["Freelancer Name", freelancer_name],
        ["Freelancer Address", freelancer_address],
        ["Invoice ID", invoice_id],
        # Additional rows for itemized invoice (items, prices, taxes, etc.)
    ]

    for item in itemized_data:
        invoice_data.append(["Item", item[0]])
        invoice_data.append(["Price", item[1]])
        invoice_data.append(["Tax", item[2]])

    # Create a Table object and set its style
    invoice_table = Table(invoice_data)
    invoice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Add the table to the PDF document
    pdf.build([invoice_table])
