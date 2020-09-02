# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Contract for School",
    "version": "12.0.3.1.0",
    "category": "Contract Management",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "contract",
        "contract_payment_mode",
        "education",
        "contacts_school",
        "contacts_school_education",
        "account_payment_order",
        "sale"
    ],
    "data": [
        "views/account_invoice_view.xml",
        "views/contract_contract_view.xml",
        "views/contract_line_view.xml",
        "wizards/account_payment_line_create_view.xml",
        "views/contract_school_menu.xml",
    ],
    "installable": True,
}
