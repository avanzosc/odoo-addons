
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
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


class product_product(osv.osv):
    _inherit = 'product.product' 
    #TRIGGER 
    #<ref_interna = default_code>
    def onchange_code(self,cr,uid,ids,code):
        value = {
          'ref_interna': code       
        }
        return {'value': value}
    
    #Miro si el codigo es númerico y de 10 dígitos.
    def _check_code(self, cr, uid, ids, context=None):
        valor = False
        #print ids
        for product in self.browse(cr,uid,ids):
            if product.default_code:
                valor = True
                if (product.default_code).isnumeric and (len(str(product.default_code))==10):
                    valor = True
                else:
                    valor=False
            else : valor = True
            
                
        return valor
            
    _columns = {
            'ref_interna':fields.char('Ref.Interna',size=64),
            }
    
    _constraints=[
                 (_check_code,'Error: Referencia is not numeric or length < 10',['code']),
        ]
product_product()    