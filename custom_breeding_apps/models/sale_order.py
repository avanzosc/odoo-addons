# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def default_type_id(self):
        result = False
        type = self.env["sale.order.type"].search(
            [("company_id", "=", self.env.company.id)]
        )
        if type and len(type) == 1:
            result = type.id
        return result

    type_id = fields.Many2one(default=default_type_id)

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            if not order.company_id.tolvasa:
                for line in order.picking_ids:
                    line.custom_date_done = fields.Datetime.now()
            mother = self.env["stock.picking.batch"].search(
                [
                    ("batch_type", "=", "breeding"),
                    ("warehouse_id", "=", order.warehouse_id.id),
                    ("company_id", "=", order.company_id.id),
                ]
            )
            if mother and len(mother) == 1:
                for picking in order.picking_ids:
                    picking.batch_id = mother.id
                    picking.button_force_done_detailed_operations()
                    for moveline in picking.move_line_ids_without_package:
                        if moveline.product_id.live_chicken:
                            lot = self.env["stock.production.lot"].search(
                                [
                                    ("product_id", "=", moveline.product_id.id),
                                    ("name", "=", picking.batch_id.name),
                                    ("company_id", "=", picking.company_id.id),
                                ],
                                limit=1,
                            )
                            if not lot:
                                lot = self.env["stock.production.lot"].create(
                                    {
                                        "name": picking.batch_id.name,
                                        "product_id": moveline.product_id.id,
                                        "company_id": picking.company_id.id,
                                    }
                                )
                            moveline.lot_id = lot.id
        return result

    def action_view_payments(self):
        result = super().action_view_payments()
        result["context"].update({"default_ref": self.env.user.name})
        return result
