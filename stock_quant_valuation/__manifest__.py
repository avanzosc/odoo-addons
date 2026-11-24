# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Quant Valuation",
    "summary": "Product and lot cost valuation in stock quants",
    "version": "18.0.1.1.0",
    "category": "Inventory/Inventory",
    "post_init_hook": "post_init_recompute",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["stock_lot_purchase_info", "purchase_last_price_info"],
    "data": ["views/stock_quant_view.xml", "views/stock_lot_view.xml"],
    "installable": True,
}
