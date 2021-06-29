## Swiss E-Invoicing App for ERPNext By Grynn GmbH (www.grynn.ch)

Swiss ERPNext App for E-Invoice Hybrid PDF based on Factur-X and ZugFerd. The PDF is fully compatible with ZugFerd and contains `factur-x.xml` according to the invoice.


## Limitations

- Sales Taxes and Charges Table should ONLY CONTAIN TAX/VAT Element. 
- No Charges should be added in this section as Factur-X / ZugFERD does not accept TAX/VAT at header level
- This limitation will NOT break ERPNext functionality but will generate a non-valid e-invoice, which will be rejected by your customer.


## Get App

```sh
bench get-app https://github.com/Grynn-GmbH/Swiss-E-invoicing-ERPNext
bench --site <your site> install-app swiss_factur_x_e_invoicing
```

## How to Use
- App Automatically Creates `e-invoice` on sales invoice submission & attachs to the PDF. 
- Company Name / Company Address / Company Tax ID are required to be present. 
- There is no settings or configuration needs to provide for this app

#### License

GPL V3
