# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    amount_type = fields.Selection(
        selection=[("cost", "Cost"), ("revenue", "Revenue")],
        compute="_compute_amount_type",
        string="Cost/Revenue",
        store=True,
    )
    account_move_id = fields.Many2one(
        string="Invoice",
        comodel_name="account.move",
        related="move_id.move_id",
        store=True,
    )
    invoice_name = fields.Char(
        string="Invoice Number", related="move_id.move_id.name", store=True
    )
    invoice_reference = fields.Char(
        string="Invoice Vendor Reference", related="move_id.move_id.ref", store=True
    )
    invoice_partner_id = fields.Many2one(
        string="Invoice Partner",
        comodel_name="res.partner",
        related="move_id.move_id.partner_id",
        store=True,
    )
    invoice_user_id = fields.Many2one(
        string="Invoice Salesperson",
        comodel_name="res.users",
        related="move_id.move_id.user_id",
        store=True,
    )

    @api.depends("amount")
    def _compute_amount_type(self):
        for line in self:
            line.amount_type = "cost" if line.amount < 0 else "revenue"
