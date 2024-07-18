from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import win32print
import win32api
import os
from datetime import datetime

def generate_and_print_pdf(request):
    # Get parameters from the request
    number = request.GET.get('number', '0001')
    datetime_str = request.GET.get('datetime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    date_to_print = request.GET.get('datekasir', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    toko = request.GET.get('toko', 'TOKO KUE')
    kasir = request.GET.get('kasir', 'Default Cashier')
    pembayaran = request.GET.get('pembayaran', '0.00')
    total = request.GET.get('total', '0.00')
    metode_bayar = request.GET.get('metode_bayar', 'Cash')
    kembalian = request.GET.get('kembalian', '0.00')

    # Define the file path
    pdf_path = 'receipt.pdf'
    y = 1600
    # Create a PDF file
    c = canvas.Canvas(pdf_path, pagesize=(250, y))  # 250 points = 80mm width
    c.setFont("Helvetica",13)
    
    # Function to draw justified text
    def draw_justified_text(c, text_left, text_right, y):
        c.drawString(10, y, text_left)
        text_width = c.stringWidth(text_right, "Helvetica",13)
        c.drawString(250 - 10 - text_width, y, text_right)
    
    
    y -= 20
    
    # Add content to the PDF
    c.drawString(10, y, toko)
    y -= 20
    c.drawString(10, y, datetime_str)
    y -= 20
    c.drawString(10, y, number)
    y -= 20
    c.drawString(10, y, "-"*60)
    y -= 20
    draw_justified_text(c, "Total Pembayaran:", f"Rp.{pembayaran}", y)
    y -= 20
    c.drawString(10, y, "-"*60)
    y -= 20
    draw_justified_text(c, f"{metode_bayar}:", f"Rp.{total}", y)
    y -= 20
    draw_justified_text(c, "Kembalian:", f"Rp.{kembalian}", y)

    c.showPage()
    c.save()
    
    # Print the PDF file
    try:
        printer_name = win32print.GetDefaultPrinter()
        win32api.ShellExecute(
            0,
            "print",
            pdf_path,
            f'/d:"{printer_name}"',
            ".",
            0
        )
        print("Print job sent successfully.")
    except Exception as e:
        return HttpResponse(f"<center><h1>Gagal print dokumen : {str(e)} </h1></center>")
    
    # Return a response
    return HttpResponse("<script>window.close();</script>")
