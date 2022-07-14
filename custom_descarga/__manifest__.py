# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Descarga",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "custom_saca",
        "custom_saca_intercompany",
        "stock_move_line_force_done",
        "custom_breeding_apps"
    ],
    "data": [
        "data/saca_line_stage.xml",
        "data/partner_category.xml",
        "data/standar_price_decimal_precision.xml",
        "views/stock_move_line_view.xml",
        "views/saca_line_view.xml",
        "views/stock_move_view.xml",
    ],
    "installable": True,
}
