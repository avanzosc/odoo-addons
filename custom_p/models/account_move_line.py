# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    out_refund_from_invoice = fields.Boolean(default=False)
