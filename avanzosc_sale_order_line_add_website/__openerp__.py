# -*- coding: utf-8 -*-
# © 2016 AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Website on sale order lines",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "account_analytic_plans",
        "sale_analytic_plans",
    ],
    "author": "AvanzOSC",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
        "Ana Juaristi <ajuaristio@gmail.com>",
    ],
    "category": "Sale",
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_line_view.xml",
        "views/res_company_view.xml",
        "views/website_view.xml",
    ],
    "installable": True,
}
