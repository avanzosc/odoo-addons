# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Requisition Line Usability",
    "version": "14.0.1.0.0",
    "category": "Purchase Management",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "purchase_stock",
        "purchase_requisition",
    ],
    "data": [
        "data/price_unit_decimal_precision.xml",
        "views/purchase_requisition_views.xml",
        "views/purchase_requisition_line_view.xml",
    ],
    "installable": True,
}
