# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class CrmLead(models.Model):
    _inherit = "crm.lead"

    repair_product_id = fields.Many2one(
        string="Product to repair", comodel_name="product.product", copy=False
    )
    repair_product_qty = fields.Float(
        string="Quantity to repair", digits="Product Unit of Measure", copy=False
    )
    repair_lot_id = fields.Many2one(
        string="Lot for repair", comodel_name="stock.production.lot", copy=False
    )
    repair_order_ids = fields.One2many(
        string="Repairs",
        comodel_name="repair.order",
        copy=False,
        inverse_name="crm_lead_id",
    )
    count_repair_orders = fields.Integer(
        string="Num. Repairs",
        store=True,
        copy=False,
        compute="_compute_count_repair_orders",
    )

    @api.depends("repair_order_ids")
    def _compute_count_repair_orders(self):
        for lead in self:
            lead.count_repair_orders = len(lead.repair_order_ids)

    def action_view_repair_orders(self):
        action = self.env.ref("repair.action_repair_order_tree")
        action_dict = action and action.read()[0]
        action_dict["context"] = safe_eval(action_dict.get("context", "{}"))
        domain = expression.AND(
            [
                [("id", "in", self.repair_order_ids.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def action_create_repair_order(self):
        if not self.partner_id:
            raise ValidationError(_("You must enter the customer."))
        if not self.repair_product_id:
            raise ValidationError(_("You must enter the product to repair."))
        if not self.repair_product_qty:
            raise ValidationError(_("You must enter the quantity to repair."))
        vals = self._get_values_to_create_repair_order()
        self.env["repair.order"].create(vals)

    def _get_values_to_create_repair_order(self):
        warehouse = self.env["stock.warehouse"].search(
            [("company_id", "=", self.company_id.id)], limit=1
        )
        vals = {
            "crm_lead_id": self.id,
            "product_id": self.repair_product_id.id,
            "product_uom": self.repair_product_id.uom_id.id,
            "product_qty": self.repair_product_qty,
            "partner_id": self.partner_id.id,
            "address_id": self.partner_id.address_get(["contact"])["contact"],
            "location_id": warehouse.lot_stock_id.id,
        }
        if self.repair_lot_id:
            vals["lot_id"] = self.repair_lot_id.id
        return vals
