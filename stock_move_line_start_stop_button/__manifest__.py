# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Stock Move Line Start Stop Button",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "hr_timesheet_stop_button",
        "stock_picking_batch_extended"
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Warehouse",
    "data": [
        "views/stock_picking_type_views.xml",
        "views/stock_picking_batch_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
}
