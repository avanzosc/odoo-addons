# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Custom Mother House Change",
    'version': '14.0.2.0.0',
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock_warehouse_farm",
        "stock_picking_batch_mother",
        "stock_picking_date_done",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_picking_batch_views.xml",
        "wizard/batch_house_change_wizard_views.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
