# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def post_init_hook(env):
    cr = env.cr
    if openupgrade.column_exists(cr, "product_pricelist_item", "pvp_price"):
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE product_pricelist_item
            SET rrp_price = pvp_price
            WHERE compute_price = 'fixed';
            """,
        )
