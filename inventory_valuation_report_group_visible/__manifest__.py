# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Inventory Valuation Report Group Visible",
    "version": "14.0.1.0.0",
    "category": "Hidden",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://www.avanzosc.es",
    "depends": [
        "stock_account",
        "product_cost_visible"
    ],
    "data": [
        "views/stock_valuation_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
