# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_origin = fields.Char(readonly=False)
