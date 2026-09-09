# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError


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
        readonly=False,
    )
    rappel_period = fields.Selection(
        related="partner_rappel_id.period",
        store=True,
    )
    rappel_amount = fields.Float(
        compute="_compute_rappel_amount",
        store=True,
    )
    rappel_product_id = fields.Many2one(
        comodel_name="product.product",
        related="partner_id.invoice_rappel_product",
        store=True,
    )
    rappel_move_id = fields.Many2one(comodel_name="account.move")

    @api.depends("partner_id", "sale_line_ids")
    def _compute_partner_rappel_id(self):
        for line in self:
            rappel = False
            if (
                line.partner_id
                and (line.sale_line_ids)
                and (line.partner_id.partner_rappel_ids)
            ):
                partner_rappels = line.partner_id.partner_rappel_ids
                rappel = partner_rappels.filtered_domain(
                    [("product_id", "=", line.product_id.id)]
                )[:1]
                if not rappel:
                    rappel = partner_rappels.filtered_domain(
                        [("product_id", "=", False)]
                    )[:1]
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

    def action_invoice_rappel_lines(self):
        lines = self.filtered(lambda line: not line.rappel_move_id)
        for partner, partner_lines in lines.grouped("partner_id").items():
            if partner and not partner.invoice_rappel_product:
                raise UserError(
                    _(
                        "The company, %s, hasn't got the rappel product.",
                        partner.name,
                    )
                )

            invoice_lines = []
            for percentage, percentage_lines in partner_lines.grouped(
                "rappel_percentage"
            ).items():
                invoice_lines.append(
                    Command.create(
                        {
                            "product_id": partner.invoice_rappel_product.id,
                            "quantity": sum(percentage_lines.mapped("quantity")),
                            "price_unit": percentage,
                        }
                    )
                )
            if not invoice_lines:
                continue

            account_move = self.env["account.move"].create(
                {
                    "move_type": "out_refund",
                    "partner_id": partner.id,
                    "sale_type_id": partner.sale_type.id,
                    "invoice_line_ids": invoice_lines,
                }
            )
            partner_lines.rappel_move_id = account_move.id
