# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2010 - 2011 Avanzosc <http://www.avanzosc.com>
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

class product_category(osv.osv):
    _inherit = 'product.category'
 
    _columns = {
        'company_id': fields.many2one('res.company', 'Company'),
    }
product_category()

class res_company(osv.osv):
    _inherit = 'res.company'
 
    _columns = {
        'cat_egg_ids': fields.many2many('product.category', 'huevo_company_rel', 'cat_huevo_id', 'company_id', 'Egg Categories'),
        'cat_chicken_ids': fields.many2many('product.category', 'gallina_company_rel', 'cat_gallina_id', 'company_id', 'Chicken Categories'),
    }
res_company()