# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Storable Generate Task",
    "version": "16.0.1.0.0",
    "category": "Banking addons",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product",
        "stock",
        "sale_timesheet",
        "sale_project",
    ],
    "data": [
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
}
