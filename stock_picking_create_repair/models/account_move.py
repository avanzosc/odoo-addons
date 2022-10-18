# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class AccountMove(models.Model):
    _inherit = "account.move"

    is_repair = fields.Boolean(
        string="Is repair", compute="_compute_is_repair")
    amount_total_products_rmas = fields.Monetary(
        string="Amount repair orders", currency_field="currency_id",
        compute="_compute_amount_total_products_rmas")
    repairs_ids = fields.One2many(
        string="Repairs", comodel_name="repair.order",
        inverse_name="invoice_id", copy=False)
    count_repairs = fields.Integer(
        string="Num. repairs", compute="_compute_count_repairs",
        store=True, copy=False)

    def _compute_is_repair(self):
        for invoice in self:
            lines = invoice.invoice_line_ids.filtered(
                lambda x: x.sale_line_id and x.sale_line_id.is_repair)
            invoice.is_repair = True if lines else False

    def _compute_amount_total_products_rmas(self):
        for invoice in self:
            if not invoice.is_repair:
                invoice.amount_total_products_rmas = 0
            else:
                amount_total_products_rmas = 0
                for line in invoice.line_ids:
                    if line.amount_products_rmas:
                        amount_total_products_rmas += line.amount_products_rmas
                invoice.amount_total_products_rmas = amount_total_products_rmas

    @api.depends("repair_ids")
    def _compute_count_repairs(self):
        for invoice in self:
            invoice.count_repairs = len(invoice.repair_ids)

    def unlink(self):
        repair_obj = self.env["repair.order"]
        for move in self:
            cond = [("invoice_id", "=", move.id)]
            repairs = repair_obj.search(cond)
            if repairs:
                repairs.write({"invoice_id": False})
        return super(AccountMove, self).unlink()

    def action_repairs_from_sale(self):
        self.ensure_one()
        action = self.env.ref("repair.action_repair_order_tree")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "in", self.repair_ids.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def get_rma_to_print(self):
        repairs = ""
        for repair in self.repairs_ids:
            repairs = (
                repair.name if not repairs else
                "{}, {}".format(repairs, repair.name))
        return repairs
