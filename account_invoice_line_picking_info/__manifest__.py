# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Invoice Line Picking Info",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "category": "Accounting & Finance",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "stock_picking_invoice_link",
        "account",
    ],
    "data": [],
    "installable": True,
    "post_init_hook": "_post_install_put_picking_in_lines",
}
