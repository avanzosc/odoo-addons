# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Forecast",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "sale_management",
        "stock",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Warehouse",
    "data": [
        "security/ir.model.access.csv",
        "data/scheduled_action.xml",
        "views/product_template_view.xml",
        "views/product_product_view.xml",
        "views/sale_order_view.xml",
        "views/product_product_stock_forecast_view.xml",
    ],
    "installable": True,
}
