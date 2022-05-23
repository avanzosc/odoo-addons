# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class Saca(models.Model):
    _inherit = "saca"

    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product")
    purchase_order_line_ids = fields.One2many(
        string="Purchase Order Lines",
        comodel_name="purchase.order.line",
        inverse_name="saca_id")
    purchase_line_count = fields.Integer(
        string="# Purchase Order Lines",
        compute="_compute_purchase_line_count")
    purchase_order_ids = fields.One2many(
        string="Purchase Order",
        comodel_name="purchase.order",
        inverse_name="saca_id")
    purchase_count = fields.Integer(
        string="# Purchase Orders",
        compute="_compute_purchase_count")

    def _compute_purchase_line_count(self):
        for saca in self:
            saca.purchase_line_count = len(saca.purchase_order_line_ids)

    def _compute_purchase_count(self):
        for saca in self:
            saca.purchase_count = len(saca.purchase_order_ids)

    def action_view_purchase_order_line(self):
        context = self.env.context.copy()
        context.update({"default_saca_id": self.id})
        return {
            "name": _("Purchase Order Lines"),
            "view_mode": "tree,form",
            "res_model": "purchase.order.line",
            "domain": [("id", "in", self.purchase_order_line_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context
        }

    def action_view_purchase_order(self):
        context = self.env.context.copy()
        context.update({"default_saca_id": self.id})
        return {
            "name": _("Purchase Orders"),
            "view_mode": "tree,form",
            "res_model": "purchase.order",
            "domain": [("id", "in", self.purchase_order_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context
        }

    def button_purchase(self):
        self.ensure_one()
        if not self.product_id:
            raise ValidationError(
                _("You must introduce the product."))
        for line in self.saca_line_ids:
            if line.supplier_id and not line.purchase_order_id:
                cond = ["|", ("saca_id", "=", self.id),
                        ("saca_id", "=", False),
                        ("partner_id", "=", line.supplier_id.id),
                        ("state", "=", "draft")]
                purchase_order = self.env["purchase.order"].search(
                    cond, limit=1)
                if not purchase_order:
                    now = fields.Datetime.now()
                    vals = {
                        "partner_id": line.supplier_id.id,
                        "date_order": now}
                    purchase_order = self.env["purchase.order"].create(vals)
                purchase_order.saca_id = self.id
                line.purchase_order_id = purchase_order.id
                if not line.purchase_order_line_id:
                    line.action_purchase_line(purchase_order)
