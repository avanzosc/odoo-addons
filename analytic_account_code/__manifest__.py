# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Analytic Account Code",
    "version": "11.0.1.0.0",
    "category": "Extra Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "analytic",
    ],
    "excludes": [
        "account_analytic_sequence",
    ],
    "data": [
        "data/account_analytic_account_data.xml",
    ],
    "installable": True,
    "post_init_hook": "assign_old_sequences",
}
