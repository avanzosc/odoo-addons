# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Crm Lead Create Repair",
    "version": "14.0.1.2.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["crm", "repair", "stock"],
    "data": [
        "views/crm_lead_views.xml",
        "views/repair_order_views.xml",
    ],
    "installable": True,
}
