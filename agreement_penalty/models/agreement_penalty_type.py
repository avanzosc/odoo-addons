# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AgreementPenaltyType(models.Model):
    _name = "agreement.penalty.type"
    _description = "Agreement Penalty Type"

    agreement_id = fields.Many2one(
        comodel_name="agreement",
        string="Agreement",
        required=True,
        ondelete="cascade",
    )
    penalty_type_id = fields.Many2one(
        comodel_name="penalty.type",
        string="Penalty Type",
        required=True,
    )
    number = fields.Integer(string="Duration Months", default=1)
    penalty_percentage = fields.Float(string="Penalty %", digits=(16, 2))
    inactive_subscription_count = fields.Integer(
        string="Inactive Subscriptions",
        default=0,
    )
    notes = fields.Text()
    product_id = fields.Many2one(
        comodel_name="product.product",
        related="penalty_type_id.product_id",
        string="Product",
        readonly=True,
    )
    penalty_price = fields.Float(string="Penalty Price", digits=(16, 2))

    @api.onchange("penalty_type_id")
    def _onchange_penalty_type_id(self):
        if self.penalty_type_id and self.penalty_type_id.product_id:
            self.penalty_price = self.penalty_type_id.product_id.list_price
