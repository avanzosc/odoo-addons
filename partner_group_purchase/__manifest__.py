# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Pedro M. Baeza
# Copyright 2016-2017 Tecnativa S.L. - Vicent Cubells
# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Purchase Group",
    "summary": "Add partner purchase group",
    "version": "16.0.1.0.0",
    "category": "Partner",
    "author": "Antiun Ingenieria & Tecnativa & AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": ["base", "sale_management", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_purchase_group_view.xml",
        "views/res_partner_purchase_group2_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
    "application": False,
}
