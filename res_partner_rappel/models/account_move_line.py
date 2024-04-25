# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    partner_rappel_id = fields.Many2one(
        string="Partner Rappel",
        comodel_name="res.partner.rappel",
        compute="_compute_partner_rappel_id",
        store=True,
    )
    rappel_percentage = fields.Float(
        string="Rappel",
        compute="_compute_rappel_percentage",
        store=True,
    )
    rappel_period = fields.Selection(
        related="partner_rappel_id.period",
        store=True,
    )
    rappel_amount = fields.Float(
        compute="_compute_rappel_amount",
        store=True,
    )

    @api.depends("partner_id", "sale_line_ids")
    def _compute_partner_rappel_id(self):
        for line in self:
            rappel = False
            if (
                line.partner_id
                and (line.sale_line_ids)
                and (line.partner_id.partner_rappel_ids)
            ):
                rappel = line.partner_id.partner_rappel_ids.filtered(
                    lambda c: c.product_id == line.product_id
                )
                if not rappel:
                    rappel = line.partner_id.partner_rappel_ids.filtered(
                        lambda c: not c.product_id
                    )
                if rappel:
                    rappel = rappel.id
            line.partner_rappel_id = rappel

    @api.depends("partner_rappel_id")
    def _compute_rappel_percentage(self):
        for line in self:
            if line.partner_rappel_id:
                line.rappel_percentage = line.partner_rappel_id.percentage

    @api.depends("rappel_percentage", "price_subtotal")
    def _compute_rappel_amount(self):
        for line in self:
            line.rappel_amount = line.rappel_percentage * line.quantity

    def action_recalcule_rappel(self):
        for line in self:
            line._compute_partner_rappel_id()
            line._compute_rappel_percentage()
