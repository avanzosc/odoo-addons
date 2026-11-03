# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Contract Sale Generation Isolation",
    "version": "16.0.1.0.0",
    "summary": (
        "Isolates recurring sale order generation contract by contract: if "
        "one fails, it is flagged and the responsible user is notified "
        "instead of aborting the rest of the daily batch."
    ),
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "category": "Sales/Contracts",
    "depends": ["contract_sale_generation"],
    "data": [
        "views/contract_contract_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
