
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
from tools.translate import _

class training_subscription_line(osv.osv):

    _inherit = 'training.subscription.line'
    _description = 'Subscription Line'
    
    def action_workflow_send_confirm(self, cr, uid, ids, context=None):
        #iker
        #OBJETOS
        ##############################################
        sale_order_obj = self.pool.get('sale.order')
        ##############################################
        
        for tsl in self.browse(cr,uid,ids):
            try:
                val = {
                      'offer_id': tsl.subscription_id.offer_id.id,
                      'partner_id':tsl.partner_id.id,
                      'session_id':tsl.session_id.id,
                      'partner_order_id':tsl.partner_id.address[0].id or null,
                      'partner_shipping_id':tsl.partner_id.address[0].id or null,
                      'partner_invoice_id':tsl.partner_id.address[0].id or null,
                      'contact_id':tsl.job_id.contact_id.id,
                      'pricelist_id':tsl.price_list_id.id,
                      'act_par':False,
                      }
                if tsl.session_id2:
                    val.update({
                                'session_id2': tsl.session_id2.id,
                                'act_par':True,
                                })
            except:
                raise osv.except_osv(_('Error!'),_('This partner has not got address'))
        new_sale_order_obj =  sale_order_obj.create(cr, uid, val, context) 
        self.write(cr,uid,ids,{'sale_order_id':new_sale_order_obj})
        val = super(training_subscription_line, self).action_workflow_send_confirm(cr,uid,ids,context=None)
        return val
    
    def _session(self, cr, uid, ids, name, args, context=None):
        res = {}
        training_subscription_line_obj = self.pool.get('training.subscription.line')
        for subscription_line in self.browse(cr, uid, ids, context=context):
            session_name=subscription_line.session_id.name
            print session_name
            res[subscription_line.id]=session_name
        return res
    
    _columns = {
                'sale_order_id': fields.many2one('sale.order','Sale Order',readonly = True),
                'session_id2':fields.many2one('training.session', 'Session2'),
                'address_id':fields.related('job_id','address_id',type='many2one',relation='res.partner.address',string='Address',store=True),
                'state_id':fields.related('address_id','state_id',type='many2one',relation='res.country.state',string='State',store=True),
                'session_name':fields.related('session_id','name',type='char',size=64,string='Session Name',store=True), 
                'address':fields.related('job_id','address_id',type='many2one',relation='res.partner.address',string='Address',store=True),                
                
               }      
training_subscription_line()