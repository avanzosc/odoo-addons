# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Packaging Type Pallet",
    "summary": "Manage packaging of pallet type",
    "version": "16.0.1.0.0",
    "category": "Stock",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "product_packaging_dimension",
    ],
    "data": [
        "views/product_packaging_view.xml",
        "views/stock_package_type_view.xml",
    ],
    "installable": True,
}
