# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Purchase Order Line Product Brand Info",
    "version": "16.0.1.0.0",
    "category": "Inventory/Purchase",
    "website": "https://github.com/avanzosc/odoo-addons",
    "author": "Avanzosc",
    "license": "AGPL-3",
    "depends": ["purchase", "product_brand_supplierinfo"],
    "data": [
        "report/purchase_order_report.xml",
        "views/purchase_order_line_views.xml",
        "views/purchase_order_views.xml",
    ],
    "installable": True,
}
