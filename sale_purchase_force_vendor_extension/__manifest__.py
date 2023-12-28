# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Purchase Force Vendor Extension",
    "version": "14.0.1.0.0",
    "category": "Hidden",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale_purchase_force_vendor",
        "base_view_inheritance_extension",
    ],
    "excludes": [],
    "data": [
        "views/sale_order_views.xml",
    ],
    "installable": True,
}
