# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Headquarter",
    'version': '14.0.1.0.0',
    "category": "Inventory/Purchase",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "res_partner_headquarter",
        "purchase",
    ],
    "data": [
        "security/purchase_order_headquarter_security.xml",
        "views/purchase_order_views.xml",
    ],
    'installable': True,
    'auto_install': True,
}
