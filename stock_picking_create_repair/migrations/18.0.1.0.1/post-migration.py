# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return
    cr.execute(
        """
        UPDATE repair_order ro
        SET sale_id = sol.order_id
        FROM sale_order_line sol
        WHERE sol.id = ro.sale_line_id
            AND ro.sale_id IS DISTINCT FROM sol.order_id
        RETURNING ro.id
        """
    )
    repair_ids = [row[0] for row in cr.fetchall()]
    _logger.info("Filled sale_id in %s repair orders", len(repair_ids))
    env = api.Environment(cr, SUPERUSER_ID, {})
    repairs = env["repair.order"].with_context(active_test=False).browse(repair_ids)
    env.add_to_compute(repairs._fields["is_repair"], repairs)
    repairs.flush_recordset()
    sales = env["sale.order"].search(
        ["|", ("repairs_count", "!=", 0), ("repair_ids", "!=", False)]
    )
    env.add_to_compute(sales._fields["repairs_count"], sales)
    sales.flush_recordset()
    _logger.info("Recomputed repairs_count in %s sale orders", len(sales))
