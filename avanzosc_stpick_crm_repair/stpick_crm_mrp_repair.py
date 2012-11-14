# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc (Daniel) <http://www.avanzosc.com>
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

from osv import fields,osv
from tools.translate import _

class stock_picking(osv.osv): 

    _description = 'stock picking Inheritance'
    _inherit = 'stock.picking'
    _columns = {
                'crm_name':fields.many2one('crm.claim',string='CRM Claim', select=True),
        }
    
    def onchange_get_address(self,cr,uid,ids,crm_name):
        v={}
        if crm_name:
            claim_obj=self.pool.get("crm.claim")
            claim=claim_obj.browse(cr,uid,crm_name)
            v['address_id']=claim.partner_id.address[0].id
        return {'value':v}
    
    def onchange_get_claim(self,cr,uid,ids,address_id):
        v={}
        claim_obj=self.pool.get("crm.claim")
        claim_ids=claim_obj.search(cr,uid,[('partner_address_id','=',address_id)],order='create_date')
        if claim_ids:
            v['crm_name']=claim_ids[len(claim_ids)-1]
        else:
            v['crm_name']=0
        return {'value':v}
stock_picking()

class mrp_repair(osv.osv): 

    _inherit = 'mrp.repair'
    _columns = {
                'crm_name':fields.many2one('crm.claim',string='CRM Claim', select=True),
        }

mrp_repair()

class crm_claim(osv.osv): 

    _description = 'CRM Claim'
    _inherit = 'crm.claim'
    _columns = {
                'st_picking': fields.one2many('stock.picking', 'crm_name', 'Stock Picking'),
                'repair_ids': fields.one2many('mrp.repair', 'crm_name', 'Stock Picking'),
        }

crm_claim()

class res_partner(osv.osv): 
    
    _inherit = 'res.partner'
    _columns = {
                'crm_claims':fields.one2many('crm.claim','partner_id', 'CRM Claims'),
        }

res_partner()


class stock_return_picking(osv.osv_memory):
    
    _inherit = 'stock.return.picking'
    
    
    def fields_view_get(self, cr, uid, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        
        record_id = context and context.get('active_id', False) or False
        res ={}
        res = super(stock_return_picking, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar,submenu=False)
        active_model = context.get('active_model')
        if  active_model != 'stock.picking':
            return res
        arch_lst=['<?xml version="1.0"?>', '<form string="%s">' % _('Return lines'), '<label string="%s" colspan="4"/>' % _('Provide the quantities of the returned products.')]
        stock_pick = self.pool.get('stock.picking').browse(cr, uid, record_id, context=context)
        if not stock_pick.crm_name : 
             #res = {'name': 'default', 'type': u'form', 'view_id': 0, 'returns': [1, 2], 'fields': {'return1': {'required': True, 'type': 'float', 'string': u'PO00002: Producto 1'}, 'return2': {'required': True, 'type': 'float', 'string': u'PO00002: Producto 2'}, 'invoice_state': {'selection': [('2binvoiced', u'Para ser abonado/facturado'), ('none', u'No facturaci\xf3n')], 'required': True, 'type': 'selection', 'string': u'Facturaci\xf3n'}}, 'model': 'stock.return.picking', 'arch': u'<?xml version="1.0"?>\n<form string="L\xedneas de devoluci\xf3n">\n<label string="Aquí va otra cosa." colspan="4"/>\n<field name="return1"/>\n<newline/>\n<field name="return2"/>\n<newline/>\n<field name="invoice_state"/>\n<newline/>\n<group col="2" colspan="4">\n<button icon="gtk-cancel" special="cancel" string="Cancel" />\n<button name="create_returns" string="Return" colspan="1" type="object" icon="gtk-apply" />\n</group>\n</form>', 'field_parent': False}
              res = {'name': 'default', 'type': u'form', 'view_id': 0, 'returns': [1, 2], 'fields': {'return1': {'required': True, 'type': 'float', 'string': u'PO00002: Producto 1'}, 'return2': {'required': True, 'type': 'float', 'string': u'PO00002: Producto 2'}, 'invoice_state': {'selection': [('2binvoiced', u'Para ser abonado/facturado'), ('none', u'No facturaci\xf3n')], 'required': True, 'type': 'selection', 'string': u'Facturaci\xf3n'}}, 'model': 'stock.return.picking', 'arch': u'<?xml version="1.0"?>\n<form string="L\xedneas de devoluci\xf3n">\n<label string="¡No se ha definido una reclamación para la devolución! " />\n<group col="2" colspan="4">\n<button icon="gtk-cancel" special="cancel" string="Cancel" />\n</group>\n</form>', 'field_parent': False}    
        return res

stock_return_picking()    
