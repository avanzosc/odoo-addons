# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Report Stock Quantity Filter Loc Categ",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Inventory/Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "product"
    ],
    "data": [
        "views/product_category_views.xml",
        "views/report_stock_quantity_views.xml",
        "views/stock_location_views.xml",
    ],
    "installable": True,
}
