import frappe
from frappe import _
from facturx import generate_from_binary
import html
from .uomcode import get_uom_code
from .constant import raw_address
from .util import app_file, convert_to_pdf_a_3, get_pdf_data, get_percentage, save_and_attach, taxAmount, totalTax


def attach_e_pdf(doc, events=None):

    company = frappe.get_doc("Company", doc.company)
    # Data For Company
    data = {
        'name': html.escape(doc.name),
        'issue_date': doc.posting_date.replace('-', ''),
        'company': html.escape(doc.company),
        'tax_id': html.escape(company.tax_id or ""),
        'customer': html.escape(doc.customer),
        'customer_name': html.escape(doc.customer_name),
        'currency': doc.currency,
        'payment_terms': html.escape(doc.payment_terms_template or ""),
        'due_date': doc.due_date.replace('-', ''),
        'total': doc.total,
        'discount': doc.discount_amount,
        'net_total': doc.net_total,
        'total_tax': doc.total_taxes_and_charges,
        'grand_total': doc.grand_total,
        'prepaid_amount': doc.total_advance,
        'outstanding_amount': doc.grand_total
    }

    data['items'] = []
    _taxes = {}

    # Create Array of Items
    for item in doc.items:
        per_item, _ = get_percentage(item, doc)
        gross_price = item.price_list_rate * item.qty
        item_data = {
            'idx': item.idx,
            'item_code': html.escape(item.item_code),
            'item_name': html.escape(item.item_name),
            'barcode': item.barcode,
            'price_list_rate': item.price_list_rate,
            'rate': item.rate,
            'unit_code': get_uom_code(item.uom),
            'qty': item.qty,
            'amount': item.amount,
            'tax_percentage': per_item,
            'gross_price': gross_price,
            'amount': item.amount
        }

        percentage, tax = get_percentage(item, doc)

        if _taxes.get(percentage) is None:
            _taxes[percentage] = {}
            _taxes[percentage]['rate'] = 0.0
            _taxes[percentage]['net_amount'] = 0.0
            _taxes[percentage]['tax_amount'] = 0.0

        _taxes[percentage]['rate'] += percentage
        _taxes[percentage]['net_amount'] += item.amount
        _taxes[percentage]['tax_amount'] += tax

        data['items'].append(item_data)

    data['taxes'] = []

    for tax in _taxes.values():
        tax_dic = {
            'rate': (tax['rate']),
            'net_amount': tax['net_amount'],
            'tax_amount': tax['tax_amount']
        }
        data['taxes'].append(tax_dic)

    # Rounding Amount
    total_tax = totalTax(_taxes)

    # Total Tax
    data['total_tax'] = total_tax

    # Rounding Off
    data['rounding_off'] = doc.total_taxes_and_charges - total_tax

    # Grand Total
    data['grand_total'] = data['grand_total'] - data['rounding_off']

    # Company
    company_address = frappe.get_doc("Address", doc.company_address)
    if company_address:

        company_address_code = frappe.get_value(
            "Country", company_address.country, "code").upper()

        data['company_address'] = {
            'address_line1': html.escape(company_address.address_line1 or ""),
            'address_line2': html.escape(company_address.address_line2 or ""),
            'pincode': html.escape(company_address.pincode or ""),
            'city': html.escape(company_address.city or ""),
            'country_code': company_address_code or "CH"
        }
    else:
        data['company_address'] = raw_address

    # Customer

    customer_address = frappe.get_doc("Address", doc.customer_address)

    if customer_address:
        customer_country_code = frappe.get_value(
            "Country", customer_address.country, "code").upper()

        data['customer_address'] = {
            'address_line1': html.escape(customer_address.address_line1 or ""),
            'address_line2': html.escape(customer_address.address_line2 or ""),
            'pincode': html.escape(customer_address.pincode or ""),
            'city': html.escape(customer_address.city or ""),
            'country_code': customer_country_code or "CH"
        }
    else:
        data['customer_address'] = raw_address

    with open(app_file('factur.html')) as f:
        xml = frappe.render_template(f.read(), data)
        pdf_temp_data = get_pdf_data(doc.doctype, doc.name)
        pdf_data = convert_to_pdf_a_3(pdf_temp_data)
        pdf = generate_from_binary(
            pdf_data, xml.encode('utf-8'), level='en16931',
            pdf_metadata={
                'author': 'Grynn GMBH',
                'keywords': 'Factur-X, Invoice',
                'title': 'Invoice',
                'subject': 'Factur-X invoice by Grynn GMBH',
            })
        save_and_attach(pdf, doc.doctype, doc.name)
