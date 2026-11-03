# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Warehouse Analysis Report Group Visible",
    "version": "14.0.2.0.0",
    "category": "Hidden",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["stock_enterprise", "product_cost_purchase_last_price_info"],
    "data": [
        "views/stock_report_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
