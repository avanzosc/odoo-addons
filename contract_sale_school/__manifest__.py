# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Contract Sale for School",
    "version": "12.0.4.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "contract_sale",
        "contract_mandate",
        "sale_school",
        "sale_school_generate_sepa",
        "contract_school",
        "product_recurring",
    ],
    "excludes": [
        "product_contract",
    ],
    "data": [
        "views/contract_contract_view.xml",
        "views/contract_line_view.xml",
        "views/sale_order_view.xml",
        "wizards/contract_line_create_view.xml",
    ],
    "installable": True,
}
