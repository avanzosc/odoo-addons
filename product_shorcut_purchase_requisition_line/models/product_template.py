# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ProductTemplate(models.Model):
    _inherit = "product.template"

    purchase_requisition_line_ids = fields.One2many(
        string="Purchase Requisition Lines",
        comodel_name="purchase.requisition.line",
        inverse_name="product_id",
    )

    purchase_requisition_line_qty = fields.Float(
        string="Purchase Requisition Lines Qty",
        digits="Product Unit of Measure",
        compute="_compute_purchase_requisition_line_qty",
    )

    def _compute_purchase_requisition_line_qty(self):
        for template in self:
            lines = template.product_variant_ids.mapped("purchase_requisition_line_ids")
            template.purchase_requisition_line_qty = sum(lines.mapped("product_qty"))

    def open_purchase_requisition_line(self):
        self.ensure_one()
        lines = self.product_variant_ids.mapped("purchase_requisition_line_ids")
        if not lines:
            return
        action = self.env["ir.actions.actions"]._for_xml_id(
            "purchase_requisition_line_menu.action_purchase_requisition_line"
        )
        domain = expression.AND(
            [
                [("id", "in", lines.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        action.update(
            {
                "domain": domain,
            }
        )
        return action
