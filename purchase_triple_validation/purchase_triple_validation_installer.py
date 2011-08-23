# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv

class purchase_triple_validation_installer(osv.osv_memory):
    _name = 'purchase.triple.validation.installer'
    _inherit = 'res.config'
    _columns = {
        'limit_amount': fields.integer('Second Maximum Purchase Amount', required=True, help="Second maximum amount after which validation of purchase is required."),
    }

    _defaults = {
        'limit_amount': 10000,
    }

    def execute(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)
        if not data:
            return {}
        amt = data[0]['limit_amount']
        data_pool = self.pool.get('ir.model.data')
        transition_obj = self.pool.get('workflow.transition')
        waiting = data_pool._get_id(cr, uid, 'purchase_triple_validation', 'trans_validated_router')
        waiting_id = data_pool.browse(cr, uid, waiting, context=context).res_id
        confirm = data_pool._get_id(cr, uid, 'purchase_triple_validation', 'trans_waiting_validated_router')
        confirm_id = data_pool.browse(cr, uid, confirm, context=context).res_id
        transition_obj.write(cr, uid, waiting_id, {'condition': 'amount_total>=%s' % (amt)})
        transition_obj.write(cr, uid, confirm_id, {'condition': 'amount_total<%s' % (amt)})
        return {}

purchase_triple_validation_installer()

class purchase_order(osv.osv):
    _inherit = 'purchase.order'
    
    STATE_SELECTION = [
        ('draft', 'Request for Quotation'),
        ('wait', 'Waiting'),
        ('confirmed', 'Waiting Approval'),
        ('validated', 'Waiting Validation'),
        ('approved', 'Approved'),
        ('except_picking', 'Shipping Exception'),
        ('except_invoice', 'Invoice Exception'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ]
    
    _columns = {
        'state': fields.selection(STATE_SELECTION, 'State', readonly=True, help="The state of the purchase order or the quotation request. A quotation is a purchase order in a 'Draft' state. Then the order has to be confirmed by the user, the state switch to 'Confirmed'. Then the supplier must confirm the order to change the state to 'Approved'. When the purchase order is paid and received, the state becomes 'Done'. If a cancel action occurs in the invoice or in the reception of goods, the state becomes in exception.", select=True),
    }
    
    def action_validated(self, cr, uid, ids, context=None):
        """ Sets state to validated.
        @return: True
        """
        self.write(cr, uid, ids, {'state':'validated'})
        return True
    
purchase_order()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

