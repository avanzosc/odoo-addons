# -*- coding: utf-8 -*-
# Copytight 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Warning by Workflow",
    "version": "8.0.1.1.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
    ],
    "category": "Tools",
    "depends": [
        "warning",
    ],
    "data": [
        "views/purchase_order_view.xml",
        "views/sale_order_view.xml",
        "views/stock_picking_view.xml",
        "wizard/partner_show_warning_view.xml",
        "wizard/stock_transfer_details.xml",
    ],
    "installable": True,
}
