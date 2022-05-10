# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Date Done",
    'version': '14.0.1.0.0',
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/wiz_put_date_realized_in_picking_views.xml",
        "views/stock_picking_views.xml",
    ],
    'installable': True,
    'auto_install': False,
}
