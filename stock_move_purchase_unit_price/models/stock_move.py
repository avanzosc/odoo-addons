# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    @api.depends('purchase_price_unit', 'quantity_done')
    def _compute_purchase_price_unit(self):
        for move in self.filtered(lambda x: x.purchase_line_id):
            move.subtotal_purchase_price_unit = (
                move.purchase_price_unit * move.quantity_done)

    purchase_price_unit = fields.Float(
        string='Purchase unit price', related='purchase_line_id.price_unit',
        store=True)
    subtotal_purchase_price_unit = fields.Float(
        string='Subtotal purchase unit price', store=True,
        compute='_compute_purchase_price_unit')
