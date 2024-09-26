# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Product QR Label",
    "version": "16.0.1.0.0",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory",
    "license": "AGPL-3",
    "depends": ["stock", "product_name_length"],
    "data": [
        "data/paperformat.xml",
        "report/layout.xml",
        "report/picking_product_qr_label_report.xml",
        "report/product_product_qr_label_report.xml",
        "report/product_template_qr_label_report.xml",
        "report/stock_product_qr_label_report.xml",
    ],
    "installable": True,
}
