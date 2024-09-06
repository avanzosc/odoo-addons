{
    "name": "Stock Lock Lot",
    "version": "16.0.1.0.0",
    "summary": "Refactor stock lock lot functionality",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "LGPL-3",
    "category": "Stock",
    "depends": [
        "stock",
    ],
    "data": [
        "views/stock_move_line_views.xml",
        "views/stock_lot_views.xml",
        "views/stock_quant_manual_assign_views.xml",
        "views/stock_lot_stage_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
