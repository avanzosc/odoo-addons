# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Batch CMR DECA",
    "version": "16.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock_picking_cmr",
        "stock_picking_batch",
        "stock_picking_batch_usability",
    ],
    "data": [
        "security/deca_groups.xml",
        "security/ir.model.access.csv",
        "report/stock_picking_batch_deca_report.xml",
        "data/mail_template_deca.xml",
        "views/stock_picking_batch_views.xml",
        "wizards/wiz_deca_modify_views.xml",
        "wizards/wiz_deca_cancel_views.xml",
    ],
    "installable": True,
}
