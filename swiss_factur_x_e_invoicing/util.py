import frappe


def get_pdf_data(doctype, name):
    """
    Get Print from Default Template
    """
    html = frappe.get_print(doctype, name)
    return frappe.utils.pdf.get_pdf(html)
