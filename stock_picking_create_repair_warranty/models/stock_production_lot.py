# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval
import pytz


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    expiration_date = fields.Datetime(
        string="Warranty date")
    expiration_date_without_hour = fields.Date(
        string="Warranty date without_hour", copy=False, store=True,
        compute="_compute_expiration_date_without_hour")
    warranty_repair_date = fields.Date(
        string="warranty repair date")
    repair_order_ids = fields.One2many(
        string="Repair orders", comodel_name="repair.order",
        inverse_name="lot_id")
    count_repair_orders = fields.Integer(
        string="Num. Repairs", compute="_compute_count_repair_orders")

    @api.depends("expiration_date")
    def _compute_expiration_date_without_hour(self):
        local_tz = pytz.timezone(self.env.user.tz or 'UTC')
        for lot in self:
            if lot.expiration_date:
                local_dt = lot.expiration_date.replace(
                    tzinfo=pytz.utc).astimezone(local_tz)
                lot.expiration_date_without_hour = local_dt.date()

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
