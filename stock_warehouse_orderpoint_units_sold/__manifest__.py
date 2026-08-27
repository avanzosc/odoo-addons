# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Warehouse Orderpoint Units Sold",
    "summary": "",
    "version": "16.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": ["purchase_stock"],
    "data": [
        "data/scheduled_action.xml",
        "views/res_partner_views.xml",
        "views/stock_warehouse_orderpoint_views.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_install_load_data",
}
