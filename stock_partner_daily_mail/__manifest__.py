# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Partner Daily Mail",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "product_brand",
        "stock",
        "website_sale",
    ],
    "external_dependencies": {
        "python": ["xlsxwriter"],
    },
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory/Inventory",
    "summary": "Send a daily Excel file with the available stock to contacts.",
    "data": [
        "data/mail_template_data.xml",
        "data/ir_cron_data.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
