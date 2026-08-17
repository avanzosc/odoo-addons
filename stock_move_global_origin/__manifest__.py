# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Move Global Origin",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory",
    "license": "AGPL-3",
    "depends": ["sale_purchase_inter_company_rules", "mrp"],
    "data": [
        "security/global_origin_security.xml",
        "security/ir.model.access.csv",
        "views/stock_move_line_views.xml",
        "views/stock_move_views.xml",
        "views/sale_order_views.xml",
        "views/purchase_order_views.xml",
        "views/mrp_production_views.xml",
        "views/assets.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
    "qweb": ["static/src/xml/global_origin_pivot.xml"],
}
