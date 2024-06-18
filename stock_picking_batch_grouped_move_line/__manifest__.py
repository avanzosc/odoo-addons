# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Batch Grouped Move Line",
    "version": "16.0.1.0.0",
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "http://www.avanzosc.es",
    "depends": ["stock_picking_batch"],
    "data": ["security/ir.model.access.csv", "views/stock_picking_batch_view.xml"],
    "license": "AGPL-3",
    "installable": True,
    "post_init_hook": "_post_install_group_picking_batch_move_lines",
}
