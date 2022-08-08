# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    is_repair = fields.Boolean(
        string="Is repair", default=False, copy=False)
    picking_type_repair_out_id = fields.Many2one(
        string="Picking type out for repair", copy=False,
        comodel_name="stock.picking.type")
    picking_type_repair_in_id = fields.Many2one(
        string="Picking type in for repair", copy=False,
        comodel_name="stock.picking.type")

    @api.onchange('is_repair')
    def _onchange_product_id(self):
        for t in self:
            if not t.is_repair:
                t.picking_type_repair_in_id = False
                t.picking_type_repair_out_id = False
