import frappe
from os import path,


def get_pdf_data(doctype, name):
    """
    Get Print from Default Template
    """
    html = frappe.get_print(doctype, name)
    return frappe.utils.pdf.get_pdf(html)


def get_xml_path():
    app_dir = path.dirname(path.realpath(__file__))
