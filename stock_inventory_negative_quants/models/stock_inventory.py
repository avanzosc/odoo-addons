# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class StockInventory(models.Model):

    _inherit = 'stock.inventory'

    delete_negative_quants = fields.Boolean(string='Delete Negative Quants')


class StockInventoryLine(models.Model):

    _inherit = 'stock.inventory.line'

    @api.model
    def _get_quants(self, line):
        quants_obj = self.env['stock.quant']
        quants_ids = super(StockInventoryLine, self)._get_quants(line)
        quants = quants_obj.browse(quants_ids)
        if line.inventory_id.delete_negative_quants and line.product_qty == \
                sum([x.qty for x in quants]):
            negative_quants = quants.filtered(lambda x: x.qty < 0)
            quants = quants.filtered(lambda x: x.qty >= 0)
            if negative_quants:
                negative_quants.with_context(force_unlink=True).sudo().unlink()
        return quants.ids
