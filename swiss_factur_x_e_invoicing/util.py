import json
import frappe
from frappe.utils.file_manager import save_file
from os import path


def taxAmount(txt):
    js = json.loads(txt)
    total_base = 0
    total_tax = 0
    for entry in js.values():
        if round(entry[0]) == 0:
            continue
        amt = (entry[1] * 100)/entry[0]
        total_base += amt
        total_tax += entry[1]

    return round(total_base, 2), round((total_tax/total_base * 100), 2)

# TODO: Fix This


def get_percentage(item, doc):
    if item.item_tax_rate is not None:
        item_tax = json.loads(item.item_tax_rate)
        return item_tax[list(item_tax.keys())[0]]
    return doc.taxes[0].rate


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
    file_name = "{}.pdf".format(to_name.replace(" ", "-"))
    save_file(file_name, content, to_doctype, to_name,  is_private=1)


def app_dir():
    return path.dirname(path.realpath(__file__))


def get_xml_path():
    appdir = app_dir()
    return path.join(appdir, 'factur.html')


def app_file(file):
    return path.join(app_dir(), file)
