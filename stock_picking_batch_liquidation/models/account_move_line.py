# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    price_unit = fields.Float(digits="Account Line Price Decimal Precision")
    name = fields.Char(string="Description")
    percentage = fields.Float(string="Percentage")
    sale_type_id = fields.Many2one(
        string="Sale Type",
        comodel_name="sale.order.type",
        related="move_id.sale_type_id",
        store=True,
    )

    @api.onchange("percentage", "move_id")
    def onchange_invoicing_qty(self):
        if self.percentage and self.move_id.invoicing_qty:
            self.quantity = self.percentage * self.move_id.invoicing_qty / 100
