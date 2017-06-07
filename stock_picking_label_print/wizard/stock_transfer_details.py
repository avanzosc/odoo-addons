# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class StockTransferDetails(models.TransientModel):

    _inherit = 'stock.transfer_details'

    @api.one
    def do_detailed_transfer(self):
        report_data_model = self.env['stock.label.report.data']
        res = super(StockTransferDetails, self).do_detailed_transfer()
        for prod in self.item_ids:
            report_data = {
                'product_id': prod.product_id.id,
                'product_qty': prod.quantity,
                'ul_id': prod.ul_id.id,
                'ul_qty': prod.ul_qty,
                'lot_id': prod.lot_id.id,
                'picking_id': self.picking_id.id,
            }
            report_data_model.create(report_data)
        return res


class StockTransferDetailsItems(models.TransientModel):

    _inherit = 'stock.transfer_details_items'

    ul_id = fields.Many2one(comodel_name='product.ul', string='Package type')
    ul_qty = fields.Integer(string='Package Quantity', default=0)
