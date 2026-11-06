# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

from odoo.tools.sql import column_exists

column_renames = {
    "product_catalog": [("visible_slider", "is_published")],
}


@openupgrade.migrate()
def migrate(env, version):
    """Rename the column to keep the old value."""
    if column_exists(env.cr, "product_catalog", "visible_slider"):
        openupgrade.rename_columns(env.cr, column_renames)
