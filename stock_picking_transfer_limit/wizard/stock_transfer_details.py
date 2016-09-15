# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, _


class StockTransferDetails(models.TransientModel):

    _inherit = 'stock.transfer_details'

    @api.model
    def default_get(self, fields):
        res = super(StockTransferDetails, self).default_get(fields=fields)
        for item in res.get('item_ids', []):
            item['origin_qty'] = item.get('quantity', 0)
        return res


class StockTransferDetailsItems(models.TransientModel):

    _inherit = 'stock.transfer_details_items'

    origin_qty = fields.Float(string="Origin qty")

    @api.multi
    @api.onchange('quantity')
    def onchange_quantity(self):
        self.ensure_one()
        res = {}
        if self.quantity > self.origin_qty:
            if self.sourceloc_id.usage == 'internal':
                self.quantity = self.origin_qty
            res = {'warning': {
                'title': _('Error in quantity'),
                'message': (_('The quantity must be lower than %s') %
                            self.origin_qty)}}
        return res
