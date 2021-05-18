# Facturx
import frappe
from frappe import _
from facturx import generate_facturx_from_file
import html
from .uomcode import get_uom_code
from .constant import raw_address
from .util import app_file


def attach_e_pdf(doc, events=None):

    # Data For Company
    data = {
        'name': html.escape(doc.name),
        # 'issue_date': "{year:04d}{month:02d}{day:02d}".format(
        #     year=company.posting_date.year, month=company.posting_date.month, day=company.posting_date.day),
        'company': html.escape(doc.company),
        'tax_id': html.escape(doc.tax_id or ""),
        'customer': html.escape(doc.customer),
        'customer_name': html.escape(doc.customer_name),
        'currency': doc.currency,
        'payment_terms': html.escape(doc.payment_terms_template or ""),
        # 'due_date': "{year:04d}{month:02d}{day:02d}".format( year=company.due_date.year, month=company.due_date.month, day=company.due_date.day),
        'total': doc.total,
        'discount': (doc.total - doc.net_total),
        'net_total': doc.net_total,
        'total_tax': doc.total_taxes_and_charges,
        'grand_total': (doc.rounded_total or doc.grand_total),
        'prepaid_amount': ((doc.rounded_total or doc.grand_total) - doc.outstanding_amount),
        'outstanding_amount': doc.outstanding_amount
    }

    data['items'] = []

    # Create Array of Items
    for item in doc.items:
        item_data = {
            'idx': item.idx,
            'item_code': html.escape(item.item_code),
            'item_name': html.escape(item.item_name),
            'barcode': item.barcode,
            'price_list_rate': item.price_list_rate,
            'rate': item.rate,
            'unit_code': get_uom_code(item.uom),
            'qty': item.qty,
            'amount': item.amount
        }
        data['items'].append(item_data)

    # Taxation
    if doc.taxes and doc.taxes[0].rate:
        data['overall_tax_rate_percent'] = doc.taxes[0].rate
        data['taxes'] = []
        for tax in doc.taxes:
            tax_data = {
                'tax_amount': tax.tax_amount,
                'net_amount': (tax.total - tax.tax_amount),
                'rate': tax.rate
            }
            data['taxes'].append(tax_data)
    else:
        data['overall_tax_rate_percent'] = 0

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

    xml = frappe.render_template(app_file('factur.html'), data)
    print(xml)
    pass
