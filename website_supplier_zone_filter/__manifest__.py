# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Supplier Zone Filter",
    "version": "13.0.1.0.0",
    "category": "website",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "portal",
        "purchase",
        "website_sale",
        "geonames_delivery_zone_link"
    ],
    "data": [
        "views/website_supplier_zone_template.xml",
        "views/website_supplier_zone_filter_template.xml",
        "views/res_partner_template.xml"
    ],
    "installable": True,
}
