# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ProductSupplierinfo(models.Model):
    _name = "product.supplierinfo"
    _inherit = [
        "product.supplierinfo",
        "portal.mixin",
        "mail.thread",
        "mail.activity.mixin",
        "utm.mixin",
    ]

    def action_get_attachment_view(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("base.action_attachment")
        cond = [("res_model", "=", "product.supplierinfo"), ("res_id", "=", self.id)]
        attachments = self.env["ir.attachment"].search(cond)
        domain = expression.AND(
            [
                [("id", "in", attachments.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        context = safe_eval(action.get("context") or "{}")
        context.update(
            {
                "default_res_model": "product.supplierinfo",
                "default_res_id": self.id,
            }
        )
        action.update(
            {
                "domain": domain,
                "context": context,
            }
        )
        return action
