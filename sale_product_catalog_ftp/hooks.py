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


def pre_init_hook(env):
    cr = env.cr

    if not _table_exists(cr, "product_catalog_ftp") or not _table_exists(
        cr, "product_catalog"
    ):
        return

    cr.execute(
        """
        DELETE FROM product_catalog_ftp f
         WHERE NOT EXISTS (
             SELECT 1 FROM product_catalog c WHERE c.id = f.catalog_id
         )
        """
    )
    if cr.rowcount:
        _logger.warning(
            "sale_product_catalog_ftp: removed %d product.catalog.ftp row(s) "
            "with no matching product.catalog (orphaned v12 data)",
            cr.rowcount,
        )
