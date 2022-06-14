# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Saca",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock_picking_batch_breeding",
        "stock_location_warehouse_usability",
        "fleet",
        "partner_contact_type",
        "vehicle_commercial_partner",
    ],
    "data": [
        "data/contact_type.xml",
        "security/ir.model.access.csv",
        "data/saca_sequence.xml",
        "data/partner_category.xml",
        "views/saca_view.xml",
        "views/saca_line_view.xml",
        "views/coya_view.xml",
        "views/fleet_vehicle_view.xml",
        "views/main_scale_view.xml",
        "views/res_partner_view.xml",
        "views/res_company_view.xml",
    ],
    "installable": True,
}
