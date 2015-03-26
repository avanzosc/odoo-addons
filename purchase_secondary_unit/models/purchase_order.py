# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    price_unit = fields.Float()
    product_uop_qty = fields.Float(
        string='Quantity (UoP)', readonly=True,
        digits=dp.get_precision('Product UoP'),
        states={'draft': [('readonly', False)]})
    product_uop = fields.Many2one(
        comodel_name='product.uom', string='Product UoP')
    product_uop_coeff = fields.Float(
        comodel_name='product.uom', string='UoM -> UoP Coeff',
        digits=dp.get_precision('Product UoP'))
    price_unit_uop = fields.Float(
        string='UoP Unit Price', readonly=True,
        digits=dp.get_precision('Product Price'),
        states={'draft': [('readonly', False)]})

    @api.onchange('price_unit')
    def onchange_price_unit(self):
        if self.product_id:
            self.price_unit_uop = self.price_unit / self.product_id.uop_coeff

    @api.onchange('price_unit_uop')
    def onchange_price_unit_uop(self):
        if self.product_id:
            self.price_unit = self.price_unit_uop * self.product_id.uop_coeff

    @api.onchange('product_uop_qty')
    def onchange_product_uop_qty(self):
        if self.product_id:
            self.product_qty = self.product_uop_qty / self.product_id.uop_coeff

    @api.onchange('product_uop')
    def onchange_product_uop(self):
        if self.product_uop == self.product_id.uop_id:
            self.product_uop_coeff = self.product_id.uop_coeff
        else:
            # TODO: See if units are of the same category
            self.product_uop_coeff = 1.0

    @api.onchange('product_uop_coeff')
    def onchange_product_uop_coeff(self):
        self.product_uop_qty = self.product_qty * self.product_uop_coeff

    def onchange_product_id(
            self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False,
            date_planned=False, name=False, price_unit=False, state='draft',
            context=None):
        res = super(PurchaseOrderLine, self).onchange_product_id(
            cr, uid, ids, pricelist_id, product_id, qty, uom_id, partner_id,
            date_order=date_order, fiscal_position_id=fiscal_position_id,
            date_planned=date_planned, name=name, price_unit=price_unit,
            state=state, context=context)
        if product_id:
            product_obj = self.pool['product.product']
            product = product_obj.browse(cr, uid, product_id, context=context)
            if product.uop_id:
                if 'value' not in res:
                    res['value'] = {}
                res['value']['product_uop'] = product.uop_id.id
        else:
            if 'value' in res:
                res['value']['product_uop'] = False
        return res
