import frappe
from os import path


def get_pdf_data(doctype, name):
    """
    Get Print from Default Template
    """
    html = frappe.get_print(doctype, name)
    return frappe.utils.pdf.get_pdf(html)


def app_dir():
    return path.dirname(path.realpath(__file__))


def get_xml_path():
    appdir = app_dir()
    return path.join(app_dir, 'factur.html')


def app_file(file):
    return path.join(app_dir(), file)
