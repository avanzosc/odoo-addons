# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ResPartner(models.Model):
    _inherit = "res.partner"

    count_pricelists_item = fields.Integer(
        string="Count Pricelist Items", compute="_compute_count_pricelists_item"
    )

    def _compute_count_pricelists_item(self):
        for partner in self.filtered(lambda c: c.property_product_pricelist):
            partner.count_pricelists_item = len(
                partner.property_product_pricelist.item_ids
            )

    def button_show_partner_pricelist_items(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "product_pricelist_item_menu.product_pricelist_item_menu_action"
        )
        domain = expression.AND(
            [
                [("pricelist_id", "=", self.property_product_pricelist.id)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        context = safe_eval(action.get("context") or "{}")
        context.update(
            {
                "search_pricelist_id": self.property_product_pricelist.id,
                "default_pricelist_id": self.property_product_pricelist.id,
            }
        )
        action.update(
            {
                "domain": domain,
                "context": context,
            }
        )
        return action
