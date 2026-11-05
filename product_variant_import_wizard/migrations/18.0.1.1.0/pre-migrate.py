# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def migrate(cr, version):
    if not openupgrade.table_exists(
        cr, "product_season"
    ) or not openupgrade.table_exists(cr, "seasonality"):
        return

    if not openupgrade.column_exists(cr, "seasonality", "code"):
        openupgrade.logged_query(
            cr, "ALTER TABLE seasonality ADD COLUMN code character varying"
        )
    openupgrade.logged_query(
        cr,
        """
        UPDATE seasonality
           SET code = RIGHT('000' || name, 3)
         WHERE code IS NULL
        """,
    )
    openupgrade.logged_query(
        cr,
        """
        INSERT INTO seasonality
            (name, code, create_uid, create_date, write_uid, write_date)
        SELECT legacy.name, legacy.name, legacy.create_uid, legacy.create_date,
               legacy.write_uid, legacy.write_date
          FROM product_season AS legacy
         WHERE NOT EXISTS (
               SELECT 1
                 FROM seasonality AS season
                WHERE season.name = legacy.name
         )
        """,
    )
    openupgrade.logged_query(
        cr,
        """
        INSERT INTO product_template_seasonality_rel
            (product_template_id, seasonality_id)
        SELECT template.id, season.id
          FROM product_template AS template
          JOIN product_season AS legacy ON legacy.id = template.season_id
          JOIN LATERAL (
               SELECT candidate.id
                 FROM seasonality AS candidate
                WHERE candidate.name = legacy.name
                ORDER BY candidate.id
                LIMIT 1
          ) AS season ON TRUE
         WHERE template.season_id IS NOT NULL
        ON CONFLICT DO NOTHING
        """,
    )
