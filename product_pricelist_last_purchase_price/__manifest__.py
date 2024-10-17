# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Pricelist Last Purchase Price",
    "version": "14.0.1.0.0",
    "category": "Inventory/Purchase",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["account", "purchase_update_pricelist"],
    "data": [
        "views/res_partner_views.xml",
        "views/product_supplierinfo_views.xml",
    ],
    "installable": True,
}
