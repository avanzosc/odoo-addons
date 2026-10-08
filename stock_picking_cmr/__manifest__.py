# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking CMR",
    "version": "18.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base_address_extended",
        "stock",
        "contacts",
        "fleet",
    ],
    "data": [
        "report/stock_picking_cmr_report.xml",
        "report/stock_picking_cmr_trasporter_report.xml",
        "views/stock_picking_views.xml",
        "views/res_partner_view.xml",
        "views/fleet_vehicle_views.xml",
    ],
    "installable": True,
}
