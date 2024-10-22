# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    purchase_order_id = fields.Many2one(
        string="Purchase Order",
        comodel_name="purchase.order",
        related="purchase_line_id.order_id",
        store=True,
        copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        if "from_purchase_order" in self.env.context:
            sequence = 0
            for vals in vals_list:
                if "sequence" in vals:
                    sequence += 10
                    vals["sequence"] = sequence
        line = super(AccountMoveLine, self).create(vals_list)
        return line
