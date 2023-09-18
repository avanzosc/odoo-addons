# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Penalty Warning",
    "version": "14.0.1.0.0",
    "category": "Inventory/Purchase",
    "author": "https://avanzosc.es/",
    "license": "AGPL-3",
    "depends": [
        "base_penalty_warning",
        "purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/penalty_warning_views.xml",
        "views/purchase_order_views.xml",
    ],
}
