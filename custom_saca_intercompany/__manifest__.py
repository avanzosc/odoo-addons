# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Saca Intercompany",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "custom_saca",
        "custom_saca_purchase",
        "purchase_sale_inter_company",
        "stock_move_line_cost",
        "sale_order_type",
        "sale_order_line_qty_by_packaging",
        "product_packaging_palet",
        "stock_move_qty_by_packaging",
    ],
    "data": [
        "views/saca_view.xml",
        "views/saca_line_view.xml",
        "views/sale_order_view.xml",
        "views/res_company_view.xml",
        "views/sale_order_type_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_move_line_view.xml",
    ],
    "installable": True,
}
