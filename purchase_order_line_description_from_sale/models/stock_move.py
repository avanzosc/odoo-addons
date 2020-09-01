# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def write(self, vals):
        result = super(StockMove, self).write(vals)
        if ('created_purchase_line_id' in vals and
                vals.get('created_purchase_line_id', False)):
            purchase_line = self.env['purchase.order.line'].browse(
                vals.get('created_purchase_line_id'))
            for move in self.filtered(lambda x: x.sale_line_id):
                if move._change_purchase_name(purchase_line):
                    purchase_line.name = move.sale_line_id.name
        return result

    def _change_purchase_name(self, purchase_line):
        valid = False
        make_to_order = self.env.ref('stock.route_warehouse0_mto')
        if (make_to_order in self.product_id.route_ids and
            self.product_id.categ_id.procured_purchase_grouping in
                ('line', 'order') and purchase_line.name !=
                self.sale_line_id.name):
            valid = True
        return valid
