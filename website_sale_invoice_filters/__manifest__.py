# Copyright 2019 Adrian Revilla - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Website sale and invoice filters",
    "version": "12.0.1.0.0",
    "category": "",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Adrian Revilla <adrianrevilla@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "website",
        "portal",
        "sale_management",
        "account",
    ],
    "data": [
        "views/website_sale_filters_template.xml",
        "views/website_invoice_filters_template.xml",
    ],
    "installable": True,
}
