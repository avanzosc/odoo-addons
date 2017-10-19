# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Risk Configuration",
    "version": "8.0.1.0.0",
    "depends": [
        "partner_financial_risk",
        "partner_sale_risk",
    ],
    "author": "Avanzosc, S.L.",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
    ],
    "category": "Sales Management",
    "website": "http://www.avanzosc.es",
    "data": [
        "data/partner_risk_configuration_data.xml",
        "views/res_partner_view.xml",
        "views/res_config_view.xml",
    ],
    "installable": True,
}
