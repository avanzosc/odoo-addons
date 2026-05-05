# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Cleaning Database Operations",
    "version": "14.0.2.1.0",
    "category": "Custom",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base",
        "base_setup",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "data/ir_config_parameter_data.xml",
        "views/cleaning_database_view.xml",
        "views/res_config_settings_view.xml",
    ],
    "installable": True,
}
