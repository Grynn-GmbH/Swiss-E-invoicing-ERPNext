# Facturx
import frappe
from frappe import _
from facturx import generate_facturx_from_file
import html


def attach_e_pdf(doc, events=None):
    company = frappe.get_doc('Company', doc.company)
    print(company.terms)
    pass
