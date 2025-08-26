# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo.tools.sql import column_exists, create_column

_logger = logging.getLogger(__name__)


def pre_init_hook(env):
    """
    Prepare new computed fields.
    """
    _logger.info("Pre-creating column last_payment_date for table account_move")
    if not column_exists(env.cr, "account_move", "last_payment_date"):
        create_column(env.cr, "account_move", "last_payment_date", "date")


def post_init_hook(env):
    """Force compute last payment date

    Since field `last_payment_date` is not automatically computed upon
    module installation, we need to compute it manually on existing records.

    :param env: an Odoo Environment instance
    """
    domain = [
        ("payment_state", "not in", ("not_paid", False)),
    ]
    invs = env["account.move"].search(domain)
    _logger.info("Force-compute last payment date on %s invoices", len(invs))
    invs._compute_last_payment_date()
