# Copyright 2023 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Picking Triple Discount Report",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Inventory/Inventory",
    "depends": [
        "stock",
        "stock_picking_report_valued",
        "sale_triple_discount",
    ],
    "data": [
        "report/deliveryslip_report.xml",
    ],
    "installable": True,
}
