# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    sale_order_type_id = fields.Many2one(
        string="Sale Order type", comodel_name="sale.order.type"
    )

    @api.onchange("customer_id")
    def onchange_customer_id(self):
        if self.customer_id.sale_type:
            self.sale_order_type_id = self.customer_id.sale_type.id
