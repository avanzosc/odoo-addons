# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Custom Breeding Apps",
    "version": "14.0.2.0.0",
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale_stock",
        "stock_warehouse_farm",
        "stock_picking_batch",
        "stock_picking_batch_mother",
        "stock_picking_batch_breeding",
        "stock_picking_batch_farmer",
        "stock_picking_date_done",
        "stock_move_line_cost",
        "custom_saca_purchase",
        "custom_saca_intercompany",
        "product_expiry",
        "purchase_order_shipping_method",
        "sale_order_line_input",
        "sale_financial_risk",
        "board",
        "account",
        "sale_order_to_payment",
        "stock_production_lot_purchase_cost",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/move_cost_decimal_precision.xml",
        "views/stock_picking_type_view.xml",
        "views/stock_move_line_view.xml",
        "views/stock_move_view.xml",
        "views/stock_warehouse_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_location_view.xml",
        "views/stock_picking_batch_view.xml",
        "views/birth_rate_view.xml",
        "views/laying_rate_view.xml",
        "views/lineage_view.xml",
        "views/estimate_weight_view.xml",
        "views/growth_rate_view.xml",
        "views/stock_quant_view.xml",
        "views/distribution_line_view.xml",
        "views/cancellation_line_view.xml",
        "views/breeding_feed_view.xml",
        "views/sale_order_line_view.xml",
        "views/purchase_order_view.xml",
        "views/product_template_view.xml",
        "views/sale_order_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
