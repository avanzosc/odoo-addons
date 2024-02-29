# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product FSC certificate",
    "version": "12.0.2.0.0",
    "category": "Hidden",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "account",
        "sale",
        "sale_stock",
    ],
    "data": [
        "data/data.xml",
        "views/product_views.xml",
        "views/account_invoice_views.xml",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
        "report/account_invoice_report_templates.xml",
        "report/sale_order_report_templates.xml",
        "report/stock_picking_report_templates.xml",
        "report/report_layout_templates.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
}
