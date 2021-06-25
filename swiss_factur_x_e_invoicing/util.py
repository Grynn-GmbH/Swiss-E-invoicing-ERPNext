import json
import subprocess
import frappe
from frappe.utils.file_manager import save_file
from os import path
import tempfile
import platform

arch, elf = platform.architecture()

file_path = path.dirname(path.realpath(__file__))


cli = path.join(
    file_path, 'gs/x64/gs') if arch == '64bit' else path.join(file_path, 'gs/x32/gs')


def taxAmount(txt, conversion_rate=1):
    js = json.loads(txt)
    total_base = 0
    total_tax = 0
    for entry in js.values():
        if round(entry[0]) == 0:
            continue
        amt = (entry[1] / conversion_rate * 100)/entry[0]
        total_base += amt
        total_tax += entry[1] / conversion_rate

    return round(total_base, 2), round((total_tax/total_base * 100), 2)


def get_percentage(item, doc):
    percentage = 0.0
    tax_amt = 0.0
    for tax in doc.taxes:
        taxes = json.loads(tax.item_wise_tax_detail)
        percentage += taxes[item.item_code][0]
        tax_amt += taxes[item.item_code][1]/doc.conversion_rate

    print(tax_amt)
    return [percentage, round(tax_amt, 2)]


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


def convert_to_pdf_a_3(pdf_data):

    with tempfile.NamedTemporaryFile(suffix='.pdf') as pdf:
        pdf.write(pdf_data)

        with tempfile.NamedTemporaryFile(suffix='.pdf') as conv_pdf:
            args = [cli, "-dPDFA=3", "-dBATCH", "-dNOPAUSE", "-dUseCIEColor", "-sProcessColorModel=DeviceCMYK",
                    "-sDEVICE=pdfwrite", "-sPDFACompatibilityPolicy=1", "-sOutputFile={}".format(conv_pdf.name), "{}".format(pdf.name)]
            subprocess.Popen(args).wait()
            return open(conv_pdf.name, 'rb').read()


def totalTax(taxes):
    base_tax = 0
    for tax in taxes.values():
        base_tax += tax['tax_amount']

    return base_tax
