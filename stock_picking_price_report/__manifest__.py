# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Picking Price Report",
    "version": "16.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "https://github.com/avanzosc/odoo-addons",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["sale", "stock", "purchase"],
    "data": [
        "report/deliveryslip_report.xml",
    ],
    "installable": True,
}
