# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Banking Mandate",
    "version": "12.0.1.0.0",
    "category": "Banking addons",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "account_banking_mandate",
        "account_banking_sepa_direct_debit",
        "account_payment_order",
    ],
    "data": [
        "wizards/res_partner_bank_mandate_generator_view.xml",
        "views/res_partner_bank_view.xml",
    ],
    "installable": True,
}
