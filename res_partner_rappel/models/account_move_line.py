# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
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

    def action_invoice_rappel_lines(self):
        ids = []
        for line in self:
            if line.partner_id and not line.partner_id.invoice_rappel_product:
                raise UserError(
                    _(
                        "The company, %s, hasn't got the rappel product.",
                        line.partner_id.name,
                    )
                )
            elif not line.rappel_move_id:
                if line.partner_id.id not in ids:
                    ids.append(line.partner_id.id)
                    account_move = self.env["account.move"].new(
                        {
                            "move_type": "out_refund",
                            "partner_id": line.partner_id.id,
                        }
                    )
                    for onchange in account_move._onchange_methods[
                        "move_type", "partner_id"
                    ]:
                        onchange(account_move)
                    vals = account_move._convert_to_write(account_move._cache)
                    account_move = self.env["account.move"].create(vals)
                    if not any(
                        [
                            line.rappel_percentage == move_line.price_unit
                            for move_line in account_move.invoice_line_ids
                        ]
                    ):
                        same_lines = self.filtered(
                            lambda c: c.partner_id == line.partner_id
                            and c.rappel_percentage == line.rappel_percentage
                        )
                        account_move_line = self.env["account.move.line"].new(
                            {
                                "product_id": line.rappel_product_id.id,
                                "quantity": sum(same_lines.mapped("quantity")),
                                "price_unit": line.rappel_percentage,
                                "move_id": account_move.id,
                            }
                        )
                        for onchange in account_move_line._onchange_methods[
                            "product_id"
                        ]:
                            onchange(account_move_line)
                        vals = account_move_line._convert_to_write(
                            account_move_line._cache
                        )
                        vals["price_unit"] = line.rappel_percentage
                        account_move.invoice_line_ids = [(0, 0, vals)]
                        for lin in same_lines:
                            lin.rappel_move_id = account_move.id
