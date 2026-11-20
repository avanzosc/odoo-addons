# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

from odoo.tools.sql import column_exists

column_renames = {
    "product_priceslist_item": [("pvp_price", "rrp_price")],
}


@openupgrade.migrate()
def migrate(env, version):
    """Rename the column ."""
    if column_exists(env.cr, "product_priceslist_item", "pvp_price"):
        openupgrade.rename_columns(env.cr, column_renames)
