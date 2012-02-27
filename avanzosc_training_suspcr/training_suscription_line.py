
# -*- encoding: utf-8 -*-
##############################################################################
#
#    AvanzOSC, Avanzed Open Source Consulting 
#    Copyright (C) 2011-2012 Iker Coranti (www.avanzosc.com). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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
from osv import fields

class training_subscription_line(osv.osv):

    _inherit = 'training.subscription.line'
    _description = 'Subscription Line'
    
    def action_workflow_send_confirm(self, cr, uid, ids, context=None):
        #OBJETOS
        ##############################################
        sale_order_obj = self.pool.get('sale.order')
        ##############################################
        for tsl in self.browse(cr,uid,ids):
            val= {
                  'partner_id':tsl.partner_id.id,
                  'session_id':tsl.session_id.id,
                  'partner_order_id':tsl.partner_id.address[0].id,
                  'partner_shipping_id':tsl.partner_id.address[0].id,
                  'partner_invoice_id':tsl.partner_id.address[0].id,
                  'contact_id':tsl.job_id.contact_id.id,
                  'pricelist_id':tsl.price_list_id.id,
                  }
        new_sale_order_obj =  sale_order_obj.create(cr,uid,val,context)   
        val = super(training_subscription_line,self).action_workflow_send_confirm(cr,uid,ids,context=None)
        return val
      
training_subscription_line()