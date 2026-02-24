# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Shortcut Purchase Rerquisition Line",
    "version": "16.0.1.0.0",
    "category": "Inventory/Purchase",
    "website": "https://github.com/avanzosc/odoo-addons",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "depends": ["product", "purchase_requisition", "purchase_requisition_line_menu"],
    "data": [
        "views/product_template_views.xml",
        "views/product_product_views.xml",
    ],
    "installable": True,
}
