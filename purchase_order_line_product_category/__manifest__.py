# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Line Product Category",
    "version": "16.0.1.0.0",
    "author": "Avanzosc",
    "category": "Inventory/Purchase",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": ["purchase_order_line_menu"],
    "data": ["views/purchase_order_line_views.xml"],
    "installable": True,
    "post_init_hook": "_post_install_put_categ_in_lines",
}
