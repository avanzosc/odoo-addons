# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tools.safe_eval import safe_eval
from odoo import _, api, fields, models
from odoo.osv import expression


class ProjectTask(models.Model):
    _inherit = "project.task"

    purchase_count = fields.Integer(
        compute="_compute_purchase_count", string="# Purchase")
    purchase_line_count = fields.Integer(
        compute="_compute_purchase_count", string="# Purchase")
    purchase_invoice_count = fields.Integer(
        compute="_compute_purchase_invoice_count", string="# Purchase Invoice")
    purchase_invoice_line_count = fields.Integer(
        compute="_compute_purchase_invoice_count", string="# Purchase Invoice")

    @api.multi
    def _get_purchase_lines(self):
        return self.env["purchase.order.line"].search([
            ("task_id", "in", self.ids)])

    @api.multi
    def _get_purchase_invoice_lines(self):
        return self.env["account.invoice.line"].search([
            ("task_id", "in", self.ids),
            ("invoice_type", "=", "in_invoice")])

    @api.multi
    def _compute_purchase_count(self):
        for task in self:
            purchase_lines = task._get_purchase_lines()
            task.purchase_count = len(purchase_lines.mapped("order_id"))
            task.purchase_line_count = len(purchase_lines)

    @api.multi
    def _compute_purchase_invoice_count(self):
        for task in self:
            invoice_lines = task._get_purchase_invoice_lines()
            task.purchase_invoice_count = len(
                invoice_lines.mapped("invoice_id"))
            task.purchase_invoice_line_count = len(invoice_lines)

    @api.multi
    def button_open_purchase_order(self):
        self.ensure_one()
        purchase_lines = self._get_purchase_lines()
        domain = [("id", "in", purchase_lines.mapped("order_id").ids)]
        return {
            "name": _("Purchase Order"),
            "domain": domain,
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "purchase.order",
        }

    @api.multi
    def button_open_purchase_order_line(self):
        self.ensure_one()
        domain = [("task_id", "in", self.ids)]
        return {
            "name": _("Purchase Order Lines"),
            "domain": domain,
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "purchase.order.line",
        }

    @api.multi
    def button_open_purchase_invoice(self):
        self.ensure_one()
        action = self.env.ref("purchase.action_invoice_pending")
        action_dict = action.read()[0] if action else {}
        lines = self._get_purchase_invoice_lines()
        domain = expression.AND([
            [("id", "in", lines.mapped("invoice_id").ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict

    @api.multi
    def button_open_purchase_invoice_line(self):
        self.ensure_one()
        domain = [("task_id", "in", self.ids)]
        return {
            "name": _("Purchase Invoice Lines"),
            "domain": domain,
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "account.invoice.line",
        }
