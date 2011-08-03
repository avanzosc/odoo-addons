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

import pooler
import wizard
from tools.translate import _


_import_done_form = '''<?xml version="1.0" encoding="utf-8"?>
<form string="Product Import">
    <separator string="Products imported" colspan="4" />
    <field name="prod_new"/>
    <newline/>
    <field name="prod_update"/>
</form>'''

_import_done_fields = {
    'prod_update': {'string':'Updated products', 'type':'float', 'readonly': True},
}

def _do_import(self, cr, uid, data, context):
    self.pool = pooler.get_pool(cr.dbname)
    esale_category_obj = self.pool.get('esale.oscom.category')
    product_obj = self.pool.get('product.product')

    product_ids = data['ids']
    category_ids_dict = {}
    products = product_obj.browse(cr, uid, product_ids)
    if len(product_ids) > 1:
        for product in products:
            product_by_category_list = category_ids_dict.get(product.categ_id.id, False)
            if product_by_category_list and len(product_by_category_list):
                product_by_category_list.append(product.id)
            else:
                category_ids_dict[product.categ_id.id] = [product.id]
        for category_id in category_ids_dict:
            web_categ_id = esale_category_obj.search(cr, uid, [('category_id','=',category_id)])
            if not len (web_categ_id):
                raise wizard.except_wizard(_('User Error'), _('Select only products which belong to a web category!'))
    else:
        oerp_category_id = products[0].categ_id.id
        web_categ_id = esale_category_obj.search(cr, uid, [('category_id','=',oerp_category_id)])

        if not len(web_categ_id):
            raise wizard.except_wizard(_('User Error'), _('This product must belong to a web category!'))

    esale_product_ids = self.pool.get('esale.oscom.product').search(cr, uid,[('product_id','in', product_ids)])
    print "en wizard, boton import tratando", esale_product_ids
    websites_ids = []
    if esale_product_ids :
        esale_prods = self.pool.get('esale.oscom.product').browse(cr, uid, esale_product_ids)
        for esale_prod in esale_prods :
            print esale_prod.web_id
            web_id = esale_prod.web_id.id
            print web_id
            if web_id not in websites_ids :
                websites_ids.append(web_id) 
                print websites_ids
 
    return product_obj.oscom_import(cr, uid, websites_ids, esale_product_ids, context=context)


class wiz_esale_oscom_import_select_products(wizard.interface):
    states = { 'init' : { 'actions' : [_do_import],
                          'result' : { 'type' : 'form',
                                       'arch' : _import_done_form,
                                       'fields' : _import_done_fields,
                                       'state' : [('end', 'End')]
                                     }
                        }
             }

wiz_esale_oscom_import_select_products('esale.oscom.import.select.products');
