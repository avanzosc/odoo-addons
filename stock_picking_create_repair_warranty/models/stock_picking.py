# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from dateutil.relativedelta import relativedelta


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        normal_sale_order_type = self.env.ref(
            "sale_order_type.normal_sale_type")
        result = super(StockPicking, self)._action_done()
        for picking in self.filtered(
            lambda x: x.state == "done" and
                x.picking_type_id.code == "outgoing"):
            if not picking.picking_type_id.is_repair:
                lines = picking.move_line_ids_without_package.filtered(
                    lambda x: x.lot_id and x.sale_line_id and
                    x.sale_line_id.order_id.type_id and
                    x.sale_line_id.order_id.type_id == normal_sale_order_type)
                for line in lines:
                    line.lot_id.expiration_date = (
                        fields.Datetime.now() + relativedelta(
                            months=line.product_id.repair_warranty_period))
            else:
                lines = picking.move_line_ids_without_package.filtered(
                    lambda x: x.lot_id and x.is_repair)
                for line in lines:
                    line.lot_id.warranty_repair_date = (
                        fields.Datetime.now() + relativedelta(
                            months=line.product_id.repair_warranty_period))
        return result
