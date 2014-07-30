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

from openerp.osv import orm, fields
import openerp.addons.decimal_precision as dp


class tax_apportionment(orm.Model):

    _name = 'tax.apportionment'
    _description = 'Tax Apportionment'

    _columns = {
        'sale_id': fields.many2one('sale.order',
                                   'Sale Order',
                                   ondelete='cascade'),
        'picking_id': fields.many2one('stock.picking',
                                      'Stock Picking',
                                      ondelete='cascade'),
        'tax_id': fields.many2one('account.tax', 'Tax'),
        'untaxed_amount':
        fields.float('Untaxed Amount',
                     digits_compute=dp.get_precision('Sale Price')),
        'taxation_amount':
        fields.float('Taxation',
                     digits_compute=dp.get_precision('Sale Price')),
        'total_amount':
        fields.float('Total',
                     digits_compute=dp.get_precision('Sale Price')),
    }
