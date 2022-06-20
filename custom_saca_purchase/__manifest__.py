# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Custom Saca Purchase",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "category": "Purchase",
    "depends": [
        "custom_saca",
        "purchase",
        "purchase_stock",
    ],
    "data": [
        "data/saca_line_stage.xml",
        "security/ir.model.access.csv",
        "views/product_template_view.xml",
        "views/saca_line_stage_view.xml",
        "views/saca_view.xml",
        "views/saca_line_view.xml",
        "views/purchase_order_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
