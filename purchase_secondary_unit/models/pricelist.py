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


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    @api.one
    @api.depends('product_id', 'product_tmpl_id')
    def _get_uop_id(self):
        if self.product_id:
            self.uop_id = self.product_id.uop_id
        elif self.product_tmpl_id:
            self.uop_id = self.product_tmpl_id.uop_id
        else:
            self.uop_id = False

    price_surcharge_uop = fields.Float(
        string='Price Surcharge for UoP',
        digits=dp.get_precision('Product Price'),
        help='Specify the fixed amount to add or substract (if negative) to'
        ' the amount calculated with the discount.')
    uop_id = fields.Many2one(
        comodel_name='product.uom', string='Unit of Purchase',
        compute=_get_uop_id, readonly=True)

    @api.onchange('price_surcharge')
    def onchange_price_surcharge(self):
        if self.product_id:
            self.price_surcharge_uop = (
                self.price_surcharge / self.product_id.uop_coeff)
        elif self.product_tmpl_id:
            self.price_surcharge_uop = (
                self.price_surcharge / self.product_tmpl_id.uop_coeff)

    @api.onchange('price_surcharge_uop')
    def onchange_price_surcharge_uop(self):
        if self.product_id:
            self.price_surcharge = (
                self.price_surcharge_uop * self.product_id.uop_coeff)
        elif self.product_tmpl_id:
            self.price_surcharge = (
                self.price_surcharge_uop * self.product_tmpl_id.uop_coeff)
