# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)


def _table_exists(cr, name):
    cr.execute(
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)",
        (name,),
    )
    return cr.fetchone()[0]


def _column_exists(cr, table, column):
    cr.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.columns
             WHERE table_name = %s AND column_name = %s
        )
        """,
        (table, column),
    )
    return cr.fetchone()[0]


def post_init_hook(env):
    cr = env.cr

    if not _table_exists(cr, "product_catalog_web"):
        return

    if not _column_exists(cr, "product_catalog_web", "visible_slider"):
        return

    _logger.info(
        "website_sale_product_catalog: copying visible_slider "
        "from product_catalog_web -> product_catalog"
    )
    cr.execute(
        """
        UPDATE product_catalog pc
           SET visible_slider = old.visible_slider
          FROM product_catalog_web old
         WHERE old.id = pc.id
        """
    )
    _logger.info(
        "website_sale_product_catalog: updated visible_slider on %d catalogs",
        cr.rowcount,
    )
