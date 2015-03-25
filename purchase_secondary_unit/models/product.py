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

from openerp import models, fields
from openerp.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uop_id = fields.Many2one(
        comodel_name='product.uom', string='Secondary Unit of Purchase',
        help='Specify a unit of measure here if purchasing is made in another'
        ' unit of measure category than inventory. Keep empty to use the'
        ' default unit of measure.')
    uop_coeff = fields.Float(
        string='Purchase Unit of Measure -> 2UoP Coeff',
        digits=dp.get_precision('Product UoP'),
        help='Coefficient to convert default Purchase Unit of Measure to'
        ' Secondary Unit of Purchase\n uop = uom * coeff', default=1.0)
