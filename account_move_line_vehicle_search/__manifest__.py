{
    "name": "Account Move Line Vehicle Search",
    "version": "14.0.1.0.0",
    "category": "Accounting",
    "summary": "Search account move lines by vehicle name and serial number ID",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
        "fleet",
        "account_fleet",
        "stock_production_lot_fleet_vehicle",
    ],
    "data": [
        "views/account_move_line_views.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
    "application": False,
}
