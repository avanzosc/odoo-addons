# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Usability",
    "version": "14.0.2.1.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
    ],
    "data": [
        "security/stock_picking_usability_groups.xml",
        "views/stock_picking_views.xml",
        "views/res_config_settings_views.xml",
        "views/stock_move_line_views.xml",
        "views/stock_move_views.xml",
    ],
    "installable": True,
}
