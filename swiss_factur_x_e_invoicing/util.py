import frappe
from frappe.utils.file_manager import save_file
from os import path


def get_pdf_data(doctype, name):
    """
    Get Print from Default Template
    """
    html = frappe.get_print(doctype, name)
    return frappe.utils.pdf.get_pdf(html)


def save_and_attach(content, to_doctype, to_name):
    """
    Attach Pdf to Doctype
    """
    file_name = "{}.pdf".format(to_name.replace(" ", "-").replace("/", "-"))
    save_file(file_name, content, to_doctype, to_name,  is_private=1)


def app_dir():
    return path.dirname(path.realpath(__file__))


def get_xml_path():
    appdir = app_dir()
    return path.join(app_dir, 'factur.html')


def app_file(file):
    return path.join(app_dir(), file)
