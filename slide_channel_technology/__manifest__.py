# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Slide Channel Technology",
    "version": "14.0.1.0.0",
    "category": "Invoices & Payments",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "website_slides",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/slide_channel_technology_category_views.xml",
        "views/slide_channel_technology_views.xml",
        "views/slide_channel_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
