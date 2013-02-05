# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
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
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv
from osv import fields
from tools.translate import _

class wiz_delete_recog(osv.osv_memory):
    _name = 'wiz.delete.recog'
    _description = 'Wizard to Delete Recog'
    
    _columns = {
        'recog_list': fields.one2many('wiz.training.recog', 'wiz_id', 'List of Recogs'),
    }
    
    def default_get(self, cr, uid, fields_list, context=None):
        #Urtzi
        values = {}
        ######################################################
        # OBJETOS #
        ######################################################
        sale_obj = self.pool.get('sale.order')
        recog_items = []
        sale = sale_obj.browse(cr, uid, context['active_id'])
        for line in sale.order_line:
            if(line.product_id.training_charges == "recog"):
                recog_items.append({
                        'product_id': line.product_id.id,
                        'name': line.product_id.name,
                        'check': True,
                        'wiz_id': 1,
                        })
        values.update({
            'recog_list': recog_items,
        })
        return values
                
    def delete_recog(self, cr, uid, ids,context=None):
        #######################################################################
        #OBJETOS#
        #######################################################################
        sale_order_obj=self.pool.get('sale.order')
        sale_order_line_obj = self.pool.get('sale.order.line')
        training_discount_line_obj=self.pool.get('training.discount.line')
        #######################################################################
        sale = sale_order_obj.browse(cr, uid, context['active_id'])
        
        for wiz in self.browse(cr, uid, ids):
            for recog in wiz.recog_list:
                if recog.check:
                    for line in sale.order_line:
                        if line.product_id==recog.product_id:
                            for discount_line in sale.discount_line_ids:
                                discount_type=discount_line.discount_type
                                if recog.product_id==discount_type:
                                    training_discount_line_obj.unlink(cr, uid,discount_line.id )
                            sale_order_line_obj.unlink(cr, uid,[line.id])        
        return {'type': 'ir.actions.act_window_close'}
wiz_delete_recog()

class wiz_training_recog(osv.osv_memory):
    _name = 'wiz.training.recog'
    _description = 'Recognition Wizard List'
 
    _columns = {
            'name':fields.char('Recognition',size=128),
            'product_id': fields.many2one('product.product', 'Product'),    
            'check': fields.boolean('Check'),
            'wiz_id': fields.many2one('wiz.delete.recog', 'Wizard'),
        }
wiz_training_recog()