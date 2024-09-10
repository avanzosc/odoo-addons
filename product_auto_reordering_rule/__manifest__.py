# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Auto Reordering Rule",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "stock",
    ],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales",
    "data": [
        "security/ir.model.access.csv",
        "wizard/wiz_create_auto_reordering_rule_view.xml",
        "views/stock_location_views.xml",
    ],
    "installable": True,
}
