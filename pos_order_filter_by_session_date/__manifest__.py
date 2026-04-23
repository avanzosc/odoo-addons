# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "POS Order Filter By Session Date",
    "version": "18.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Show only open tickets from the session opening date",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["point_of_sale"],
    "assets": {
        "point_of_sale.assets_prod": [
            "pos_order_filter_by_session_date/static/src/js/pos_store_patch.esm.js",
        ],
    },
    "installable": True,
    "license": "AGPL-3",
}
