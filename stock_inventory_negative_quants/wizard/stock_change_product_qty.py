# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class StockChangeProductQty(models.TransientModel):

    _inherit = 'stock.change.product.qty'

    delete_negative_quants = fields.Boolean(string='Delete Negative Quants')

    @api.model
    def _prepare_inventory_line(self, inventory_id, data):
        inv = self.env['stock.inventory'].browse(inventory_id)
        if data.delete_negative_quants and not inv.delete_negative_quants:
            inv.delete_negative_quants = True
        return super(StockChangeProductQty, self)._prepare_inventory_line(
            inventory_id, data)
