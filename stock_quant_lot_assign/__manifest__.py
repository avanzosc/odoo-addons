# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Quant Lot Assign",
    "summary": "Assign a new lot to the quants without lot of products that "
    "are now tracked by lots",
    "version": "18.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
    ],
    "data": [
        "data/ir_config_parameter.xml",
        "data/ir_sequence.xml",
        "data/ir_actions_server.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
