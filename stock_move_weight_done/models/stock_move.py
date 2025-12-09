# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    validated_weight = fields.Boolean(
        default=False,
        help="Mark when the weight of the product has been physically verified.",
    )
    weight_validated_by = fields.Many2one(
        comodel_name="res.users",
        string="Validated by",
        readonly=True,
    )
    weight_validated_day = fields.Datetime(
        string="Validation date",
        readonly=True,
    )

    def write(self, vals):
        if "validated_weight" in vals:
            vals.update(
                {
                    "weight_validated_by": self.env.user.id,
                    "weight_validated_day": fields.Datetime.now(),
                }
            )
        return super().write(vals)
