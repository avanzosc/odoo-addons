# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Purchase Order Line Packaging Palet",
    "version": "16.0.1.1.0",
    "category": "Inventory/Purchase",
    "license": "AGPL-3",
    "author": "https://github.com/avanzosc/odoo-addons",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase",
        "product_packaging_palet",
        "purchase_order_line_qty_by_packaging",
    ],
    "data": [
        "views/purchase_order_views.xml",
    ],
    "installable": True,
}
