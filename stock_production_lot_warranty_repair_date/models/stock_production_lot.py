# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    warranty_repair_date = fields.Date(
        string="warranty repair date")
    repair_order_ids = fields.One2many(
        string="Repair orders", comodel_name="repair.order",
        inverse_name="lot_id")
    count_repair_orders = fields.Integer(
        string="Num. Repairs", compute="_compute_count_repair_orders")

    def _compute_count_repair_orders(self):
        for lot in self:
            lot.count_repair_orders = len(lot.repair_order_ids)

    def action_view_repairs_from_lot(self):
        self.ensure_one()
        if self.count_repair_orders > 0:
            action = self.env["ir.actions.actions"]._for_xml_id(
                "repair.action_repair_order_tree")
            action['domain'] = [('id', 'in', self.repair_order_ids.ids)]
            action['context'] = {
                "default_lot_id": self.id,
                "search_default_lot_id": self.id,
                "default_company_id": (self.company_id or self.env.company).id,
            }
            return action
