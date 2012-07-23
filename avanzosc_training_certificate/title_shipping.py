# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    Copyright (C) 2012 Avanzosc (http://Avanzosc.com). All Rights Reserved
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

import netsvc
from osv import osv
from osv import fields

class title_shipping(osv.osv):
    
    _name = 'title.shipping'
    _description = 'Title Shipping'
    
    _columns = {
            
            'number': fields.char('Shipping Nº', size=64, required=True),
            'send_date':fields.date('Send Date'),
            'title_ids':fields.many2many('training.record','shipping_record_rel','shipping_id','record_id', 'Titles'),
            'state': fields.selection([
               ('draft','Draft'),
               ('sent','Sent'),
               ],'State', readonly=True),
    }
    _defaults = {
        'number': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'title.shipping'),
        'state':lambda *a:'draft',
    }
    
#    def _contact(self, cr, uid, ids, name, args, context=None):
#        res = {}
#        training_sale_order_obj = self.pool.get('sale.order')
#        for invoice in self.browse(cr, uid, ids, context=context):
#            order=invoice.origin
#            list_id_sale_orders = training_sale_order_obj.search(cr,uid,[('name','=', order)])
#            contact=''
#            for sale_order in training_sale_order_obj.browse(cr,uid,list_id_sale_orders,context=context):
#                contact=sale_order.contact_id.name+' '+sale_order.contact_id.lastname_two+' '+sale_order.contact_id.first_name
#            res[invoice.id]=contact
#        return res
    
    #######################################################
    ## METODOS DEL WORKFLOW ##
    #######################################################
    
    def action_open(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'draft'})
        return True
    
    def action_send(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'sent'})
        wf_service = netsvc.LocalService("workflow")
        training_record_obj = self.pool.get('training.record')
        for shipping in self.browse(cr, uid, ids, context=None):
            titles=shipping.title_ids
            for record in titles:
#                para cambiar el estado del expediente:(llamamos a la señal del workflow de training.record)
                wf_service.trg_validate(uid, 'training.record', record.id, 'button_sent_ministry', cr)
#                training_record_obj.write(cr,uid,record.id,{'state':'sent_to_ministry'})
        return True
    
    def import_file(self, cr, uid, ids, context=None):
        wf_service = netsvc.LocalService("workflow")
        training_record_obj = self.pool.get('training.record')
        for shipping in self.browse(cr, uid, ids, context=None):
            titles=shipping.title_ids
            for record in titles:
                wf_service.trg_validate(uid, 'training.record', record.id, 'button_print_pending', cr)
#                training_record_obj.write(cr,uid,record.id,{'state':'print_pending'})
        return True
 
    
title_shipping()
