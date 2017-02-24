# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "HR Contract Extra Fields",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "hr_contract",
    ],
    "author": "AvanzOSC",
    "category": "Human Resources",
    "data": [
        "security/ir.model.access.csv",
        "data/hr_payment_type.xml",
        "data/hr_payment_periodicity.xml",
        "views/hr_contract_view.xml",
    ],
    'installable': True,
}
