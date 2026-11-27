# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.table_exists(env.cr, "product_season"):
        openupgrade.logged_query(
            env.cr,
            """
            INSERT INTO seasonality (id, name) SELECT id, name FROM product_season
            ON CONFLICT (id) DO NOTHING;
            """,
        )
