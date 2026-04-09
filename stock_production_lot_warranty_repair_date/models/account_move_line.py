# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _find_repairs_to_put_invoice(self, sale_line):
        repairs = super()._find_repairs_to_put_invoice(sale_line)
        if repairs:
            repairs = repairs.filtered(lambda z: not z.in_warranty)
        return repairs
