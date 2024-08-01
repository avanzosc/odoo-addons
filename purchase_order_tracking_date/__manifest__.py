{
    "name": "Purchase Order Tracking Date",
    "version": "14.0.1.0.0",
    "summary": "Adds a purchase tracking tab to Purchase Orders",
    "category": "Purchases",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["purchase"],
    "data": [
        "views/purchase_order_view.xml",
        "views/purchase_order_carrier_view.xml",
        "security/ir.model.access.csv",
    ],
    "license": "AGPL-3",
    "installable": True,
}
