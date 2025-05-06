# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Supplierinfo Customer Code Report",
    "version": "16.0.1.0.0",
    "author": "AvanzOSC",
    "category": "Inventory",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "stock",
        "product_supplierinfo_for_customer_sale",
    ],
    "data": [
        "reports/stock_picking_operations_report.xml",
        "reports/report_delivery_document.xml",
    ],
    "installable": True,
}
