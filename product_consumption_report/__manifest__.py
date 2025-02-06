# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Consumption Report",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory",
    "depends": [
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_view.xml",
        "wizard/product_consumption_wizard_view.xml",
        "report/product_consumption_xlsx.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
