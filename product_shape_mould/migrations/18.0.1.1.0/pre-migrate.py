# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tools.sql import column_exists, rename_column


def migrate(cr, version):
    for table in ("product_shape", "product_mould"):
        if column_exists(cr, table, "code") and not column_exists(cr, table, "name"):
            rename_column(cr, table, "code", "name")
