# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class RepairOrder(models.Model):
    _inherit = "repair.order"

    created_from_move_line_id = fields.Many2one(
        string="Created from detailed operation", copy=False,
        comodel_name="stock.move.line")
    created_from_picking_id = fields.Many2one(
        string="Created from incoming picking", comodel_name="stock.picking",
        related="created_from_move_line_id.picking_id", store=True, copy=False)
    purchase_order_id = fields.Many2one(
        string="Purchase order", comodel_name="purchase.order", copy=False)
    sale_order_id = fields.Many2one(
        string="Sale order", comodel_name="sale.order", copy=False)