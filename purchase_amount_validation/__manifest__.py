# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Validation by Amount",
    "version": "11.0.1.0.0",
    "category": "Purchases",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "purchase",
    ],
    "data": [
        "security/purchase_amount_validation_groups.xml",
        "views/purchase_view.xml",
        "views/res_config_view.xml",
    ],
    "installable": True,
}
