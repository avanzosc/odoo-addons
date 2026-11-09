# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "L10n Es Deca Oca Origin",
    "version": "18.0.1.0.0",
    "category": "Stock ",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "stock",
        "fleet",
        "product_trim_name",
        "base_import_wizard",
        "sale_order_line_menu",
        "l10n_es_deca_oca",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/l10n_es_deca_oca_origin_security.xml",
        "report/report_picking_deca.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/sale_order_line_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_move_views.xml",
        "views/sale_order_import_views.xml",
        "views/sale_order_import_line_views.xml",
    ],
    "installable": True,
}
