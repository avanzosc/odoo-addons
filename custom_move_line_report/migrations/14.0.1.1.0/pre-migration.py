# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    if not openupgrade.column_exists(cr, "stock_move_line", "commercial_partner_id"):
        cr.execute(
            """
            ALTER TABLE stock_move_line
            ADD COLUMN commercial_partner_id integer;
        """
        )

    cr.execute(
        """
        UPDATE stock_move_line sml
        SET commercial_partner_id = rp.commercial_partner_id
        FROM res_partner rp
        WHERE rp.id = sml.picking_partner_id
          AND sml.commercial_partner_id IS NULL
          AND rp.commercial_partner_id IS NOT NULL
    """
    )
    if not openupgrade.column_exists(cr, "stock_move_line", "contact_sale_type_id"):
        cr.execute(
            """
            ALTER TABLE stock_move_line
            ADD COLUMN contact_sale_type_id integer;
        """
        )

    cr.execute(
        """
        UPDATE stock_move_line sml
        SET contact_sale_type_id =
            split_part(ip.value_reference, ',', 2)::int
        FROM ir_property ip
        WHERE ip.name = 'sale_type'
          AND ip.res_id = 'res.partner,' || sml.picking_partner_id
          AND ip.company_id = sml.company_id
          AND sml.contact_sale_type_id IS NULL
          AND ip.value_reference LIKE 'sale.order.type,%'
    """
    )
