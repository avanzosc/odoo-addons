# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Sale Partner Category Restriction",
    "summary": "Restrict payment providers and delivery methods to customers "
    "with given tags",
    "version": "18.0.1.0.0",
    "category": "Website/Website",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "website_sale",
    ],
    "data": [
        "views/payment_provider_views.xml",
        "views/delivery_carrier_views.xml",
    ],
    "installable": True,
}
