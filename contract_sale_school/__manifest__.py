# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Contract Sale for School",
    "version": "12.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "contract_sale",
        "sale_crm_school",
        "contract_school",
        "product_recurring"
    ],
    "data": [
        "views/account_analytic_account_view.xml",
        "views/sale_order_view.xml",
    ],
    "installable": True,
}
