# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _compute_count_requisitions(self):
        for sale in self:
            sale.count_requisitions = len(sale.purchase_requisition_ids)

    purchase_requisition_ids = fields.One2many(
        comodel_name='purchase.requisition', inverse_name='sale_order_id',
        string='Calls for bids')
    count_requisitions = fields.Integer(
        compute='_compute_count_requisitions', string='Calls for bids')

    @api.multi
    def button_create_purchase_requision_from_sale_order(self):
        prequisition_obj = self.env['purchase.requisition']
        for sale in self.filtered(lambda x: x.order_line):
            prequisition_vals = {'origin': sale.name,
                                 'sale_order_id': sale.id}
            line_ids = []
            for line in sale.order_line:
                prequisition_line_vals = {
                    'product_id': line.product_id.id,
                    'product_qty': line.product_uom_qty,
                    'product_uom_id': line.product_uom.id,
                    'sale_order_line_id': line.id}
                line_ids.append((0, 0, prequisition_line_vals))
            prequisition_vals['line_ids'] = line_ids
            prequisition_obj.create(prequisition_vals)

    @api.multi
    def show_calls_for_bids(self):
        self.ensure_one()
        return {'name': _('Calls for bids'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'purchase.requisition',
                'domain': [('id', 'in', self.purchase_requisition_ids.ids)]}
