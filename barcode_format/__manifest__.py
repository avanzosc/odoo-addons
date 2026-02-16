{
    "name": "Barcode Format",
    "version": "14.0.1.0.0",
    "category": "Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "base",
        "stock",
        "contacts",
        "base_gs1_barcode",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/barcode_format_security.xml",
        "views/barcode_format_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
