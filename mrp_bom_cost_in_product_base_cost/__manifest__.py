# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "MRP BoM Cost In Product Base Cost",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "product_category_sale_price",
        "mrp_bom_cost"
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Sales",
    "data": [
        "views/product_product_view.xml",
        "wizard/stock_change_standard_price_views.xml",
        "wizard/wiz_product_template_recalculate_bom_cost_view.xml",
        "wizard/wiz_product_product_recalculate_bom_cost_view.xml",
        "wizard/wiz_product_product_recalculate_bom_cost2_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
