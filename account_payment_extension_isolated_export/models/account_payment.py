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
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################


from osv import osv
from tools.translate import _


class payment_order(osv.osv):

    _inherit = 'payment.order'

    def launch_wizard(self, cr, uid, ids, context=None):
        orders = self.browse(cr, uid, ids, context)
        order = orders[0]
        if not context:
            context = {}
        if order.mode.type and order.mode.type.ir_model_id:
            return super(payment_order, self).launch_wizard(cr, uid, ids,
                                                            context=context)
        else:
            context.update({'active_model': 'payment.order',
                            'active_ids': ids,
                            'active_id': ids[0]})
            return {'name': _('Create Payments File'),
                    'res_model': 'wizard.payment.file.spain',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'nodestroy': True,
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': context
                    }
payment_order()
