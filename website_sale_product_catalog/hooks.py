# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo.tools.sql import column_exists, table_exists

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    cr = env.cr

    if not table_exists(cr, "product_catalog_web"):
        return

    if not column_exists(cr, "product_catalog_web", "visible_slider"):
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
