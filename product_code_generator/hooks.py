# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)

STALE_INDEXES = [
    "product_category__property_account_income_categ_id_index",
]


def pre_init_hook(env):
    from openupgradelib import openupgrade

    cr = env.cr
    for index in STALE_INDEXES:
        openupgrade.logged_query(cr, f'DROP INDEX IF EXISTS "{index}"')

    _migrate_legacy_seasons(cr, openupgrade)


def _migrate_legacy_seasons(cr, openupgrade):
    if not openupgrade.table_exists(
        cr, "product_season"
    ) or not openupgrade.table_exists(cr, "seasonality"):
        return

    cr.execute("SELECT COUNT(*) FROM seasonality")
    if cr.fetchone()[0]:
        _logger.warning(
            "seasonality already has data, skipping the id-preserving "
            "migration from the legacy product_season table"
        )
        return

    if not openupgrade.column_exists(cr, "seasonality", "code"):
        openupgrade.logged_query(
            cr, "ALTER TABLE seasonality ADD COLUMN code character varying"
        )

    openupgrade.logged_query(
        cr,
        """
        INSERT INTO seasonality
            (id, name, code, create_uid, create_date, write_uid, write_date)
        SELECT id, name, name, create_uid, create_date, write_uid, write_date
        FROM product_season
        """,
    )
    openupgrade.logged_query(
        cr,
        """
        SELECT setval(
            pg_get_serial_sequence('seasonality', 'id'),
            COALESCE((SELECT MAX(id) FROM seasonality), 1)
        )
        """,
    )

    for table, constraint in (
        ("product_template", "product_template_season_id_fkey"),
        ("product_code", "product_code_season_id_fkey"),
    ):
        if openupgrade.table_exists(cr, table):
            openupgrade.logged_query(
                cr,
                f'ALTER TABLE "{table}" DROP CONSTRAINT IF EXISTS "{constraint}"',
            )
