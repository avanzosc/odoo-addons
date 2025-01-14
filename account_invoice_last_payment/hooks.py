# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

try:
    from openupgradelib import openupgrade
except Exception:
    from odoo.tools import sql as openupgrade

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    Prepare new computed fields.
    """
    _logger.info("Pre-creating column last_payment_date for table account_move")
    if not openupgrade.column_exists(cr, "account_move", "last_payment_date"):
        cr.execute(
            """
            ALTER TABLE account_move
            ADD COLUMN last_payment_date DATE;
            COMMENT ON COLUMN account_move.last_payment_date
            IS 'Last Payment Date';
            """
        )


def post_init_hook(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        force_compute_last_payment_date(env)


def force_compute_last_payment_date(env):
    """Force compute last payment date

    Since field `last_payment_date` is not automatically computed upon
    module installation, we need to compute it manually on existing records.

    :param env: an Odoo Environment instance
    """
    domain = [
        ("payment_state", "not in", ("not_paid", False)),
    ]
    invs = env["account.move"].search(domain)
    _logger.info("Force-compute last payment date on %s invoices" % len(invs))
    invs._compute_last_payment_date()
