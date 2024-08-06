# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Event Registration Student",
    "version": "16.0.1.0.0",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Sales/CRM",
    "depends": [
        "event",
        "education_center",
        "event_schedule",
        "event_registration_sale_line_contract",
    ],
    "data": [
        "data/email_template_data.xml",
        "views/event_registration_views.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
