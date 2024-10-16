# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Valuation Layer Filter Loc Categ",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "category": "Inventory/Inventory",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": ["stock_account", "report_stock_quantity_filter_loc_categ"],
    "data": [
        "views/stock_valuation_layer_views.xml",
    ],
    "installable": True,
    "auto_install": True,
    "post_init_hook": "load_data_into_stock_valuation_layer",
}
