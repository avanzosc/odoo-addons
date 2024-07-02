# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    product_packaging_qty = fields.Float(string="Product packaging qty", copy=False)
