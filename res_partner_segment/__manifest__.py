# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Res Partner Segment",
    "version": "18.0.1.0.0",
    "category": "Sales/CRM",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/partner_segment_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
