# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from ast import literal_eval

from odoo import fields, models
from odoo.osv import expression


class ProductProduct(models.Model):
    _inherit = "product.product"

    nbr_reordering_weekday_rules = fields.Integer(
        string="Reordering Weekday Rules",
        compute="_compute_nbr_reordering_weekday_rules",
        compute_sudo=False,
    )

    def _compute_nbr_reordering_weekday_rules(self):
        read_group_res = self.env["stock.warehouse.orderpoint.weekday"].read_group(
            [("product_id", "in", self.ids)], ["product_id"], ["product_id"]
        )
        res = {i: {} for i in self.ids}
        for data in read_group_res:
            res[data["product_id"][0]]["nbr_reordering_weekday_rules"] = int(
                data["product_id_count"]
            )
        for product in self:
            product_res = res.get(product.id) or {}
            product.nbr_reordering_weekday_rules = product_res.get(
                "nbr_reordering_weekday_rules", 0
            )

    def action_view_weekday_orderpoints(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock_orderpoint_weekday.action_orderpoint_weekdays_tree"
        )
        action["context"] = literal_eval(action.get("context"))
        if self and len(self) == 1:
            action["context"].update(
                {
                    "default_product_id": self.ids[0],
                    "search_default_product_id": self.ids[0],
                }
            )
        else:
            action["domain"] = expression.AND(
                [action.get("domain", []), [("product_id", "in", self.ids)]]
            )
        return action


class ProductTemplate(models.Model):
    _inherit = "product.template"

    nbr_reordering_weekday_rules = fields.Integer(
        string="Reordering Weekday Rules",
        compute="_compute_nbr_reordering_weekday_rules",
        compute_sudo=False,
    )

    def _compute_nbr_reordering_weekday_rules(self):
        res = {k: {"nbr_reordering_weekday_rules": 0} for k in self.ids}
        product_data = self.env["stock.warehouse.orderpoint.weekday"].read_group(
            [("product_id.product_tmpl_id", "in", self.ids)],
            ["product_id"],
            ["product_id"],
        )
        for data in product_data:
            product = self.env["product.product"].browse([data["product_id"][0]])
            product_tmpl_id = product.product_tmpl_id.id
            res[product_tmpl_id]["nbr_reordering_weekday_rules"] += int(
                data["product_id_count"]
            )
        for template in self:
            if not template.id:
                template.nbr_reordering_weekday_rules = 0
                continue
            template.nbr_reordering_weekday_rules = res[template.id][
                "nbr_reordering_weekday_rules"
            ]

    def action_view_weekday_orderpoints(self):
        return self.product_variant_ids.action_view_weekday_orderpoints()
