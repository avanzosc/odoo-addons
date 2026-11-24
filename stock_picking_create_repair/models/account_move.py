# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class AccountMove(models.Model):
    _inherit = "account.move"

    is_repair = fields.Boolean(
        string="Is repair",
        compute="_compute_is_repair",
    )
    amount_total_products_rmas = fields.Monetary(
        string="Amount repair orders",
        currency_field="currency_id",
        compute="_compute_amount_total_products_rmas",
    )
    repairs_ids = fields.One2many(
        string="Repairs",
        compute="_compute_repairs_ids",
        comodel_name="repair.order",
        store=False,
    )
    count_repairs = fields.Integer(
        string="Num. repairs", compute="_compute_count_repairs", store=False
    )

    def _compute_is_repair(self):
        for invoice in self:
            lines = invoice.invoice_line_ids.filtered(
                lambda x: x.sale_line_id and x.sale_line_id.is_repair
            )
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

    def _compute_repairs_ids(self):
        for account_move in self:
            sale_orders = account_move.mapped("line_ids.sale_line_ids.order_id")
            invoices = sale_orders.mapped("repair_order_ids")
            account_move.repairs_ids = invoices

    def _compute_count_repairs(self):
        for invoice in self:
            invoice.count_repairs = len(invoice.repairs_ids)

    def action_repairs_from_sale(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "repair.action_repair_order_tree"
        )
        action["domain"] = expression.AND(
            [
                [("id", "in", self.repair_ids.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        return action

    def get_rma_to_print(self):
        repairs = ""
        for repair in self.repairs_ids:
            repairs = repair.name if not repairs else f"{repairs}, {repair.name}"
        return repairs
