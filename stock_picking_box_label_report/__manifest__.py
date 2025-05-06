# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Box Label Report",
    "version": "16.0.1.0.0",
    "author": "AvanzOSC",
    "category": "Inventory",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["stock", "product_supplierinfo_for_customer"],
    "data": [
        "security/ir.model.access.csv",
        "data/paperformat.xml",
        "wizard/wiz_picking_box_label_views.xml",
        "reports/layout.xml",
        "reports/picking_box_label_report.xml",
    ],
    "installable": True,
}
