# Copyright 2020 Adrian Revilla - AvanzOSC
# Copyright 2025 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Date Ready Fordwarded",
    "version": "18.0.1.0.0",
    "category": "Purchases",
    "summary": """Adds ready, forwarded, delivery and arrival dates
    to purchase orders for enhanced supply chain tracking""",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "contributors": [
        "Adrian Revilla <adrianrevilla@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "purchase",
    ],
    "data": [
        "report/purchase_order_reports.xml",
        "views/purchase_order_views.xml",
    ],
    "installable": True,
}
