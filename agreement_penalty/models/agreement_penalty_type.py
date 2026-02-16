# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


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
    number = fields.Integer(string="Duration", default=1)
    term = fields.Selection(
        selection=[
            ("days", "Days"),
            ("months", "Months"),
            ("years", "Years"),
        ],
        default="months",
        required=True,
    )
    penalty_percentage = fields.Float(string="Penalty %", digits=(16, 2))
    active_subscription_count = fields.Integer(
        string="Active Subscriptions",
        default=0,
    )
    notes = fields.Text(string="Notes")
