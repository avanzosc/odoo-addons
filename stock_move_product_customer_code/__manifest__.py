# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Move Product Customer Code",
    "version": "16.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "https://github.com/avanzosc/odoo-addons",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "product",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/stock_picking_views.xml",
        "report/deliveryslip_report.xml",
        "report/stockpicking_operations_report.xml",
    ],
    "installable": True,
}
