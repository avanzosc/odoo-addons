# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2008-2013 AvanzOSC S.L. All Rights Reserved
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
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp.osv import orm, fields


class module_extra_documentation(orm.Model):

    _name = 'module.doc'


class module_extra_documentation_links(orm.Model):

    _name = 'module.doc.link'
    _description = 'Extra documentation - Links'

    _columns = {
        'desc': fields.char('Description', size=256),
        'link': fields.char('Link', size=256),
        'doc_id': fields.many2one('module.doc','Extra documentation', required=True, translate=True),
    }


class module_extra_documentation_categories(orm.Model):
    
    _name = 'module.doc.mod_category'

    _columns = {
        'name': fields.char('Category name', size=256, required=True, translate=True),
        'doc_ids': fields.many2many('module.doc', 'rel_doc_categories', 'category_id', 'doc_id', 'Extra documentation'),
    }


class module_extra_documentation_industries(orm.Model):
    
    _name = 'module.doc.industry'
    
    _columns = {
        'name': fields.char('Industry sector', size=256, required=True, translate=True),
        'doc_ids': fields.many2many('module.doc', 'rel_doc_industries', 'industry_id', 'doc_id', 'Extra documentation'),
    }


class module_extra_documentation_areas(orm.Model):

    _name = 'module.doc.area'
    
    _columns = {
        'name': fields.char('Area name', size=256, required=True),
        'doc_ids': fields.many2many('module.doc', 'rel_doc_areas', 'area_id', 'doc_id', 'Extra documentation'),
    }


class module_extra_documentation(orm.Model):
    
    _inherit = 'module.doc'
    
    _columns = {
        'name': fields.char('Title', size=256),
        'ext_desc_html': fields.html('Extended description (HTML)', translate=True),
        'screenshot_ids': fields.one2many('module.doc.image', 'doc_id', 'Screenshots'),
        'link_ids': fields.one2many('module.doc.link', 'doc_id', 'Links'),
        'category_ids': fields.many2many('module.doc.mod_category', 'rel_doc_categories', 'doc_id', 'category_id', 'Categories'),
        'industry_ids': fields.many2many('module.doc.industry', 'rel_doc_industries', 'doc_id', 'industry_id', 'Industries'),
        'area_ids': fields.many2many('module.doc.area', 'rel_doc_areas', 'doc_id', 'area_id', 'Areas'),
        'module_id': fields.many2one('ir.module.module', 'Module'),
        't_install': fields.float('Installation time', digits=(6,2)),
        't_config': fields.float('Configuration time', digits=(6,2)),
        't_train': fields.float('Training time', digits=(6,2)),
        't_practice': fields.float('Practice time', digits=(6,2)),
        't_start': fields.float('Start time', digits=(6,2)),
        'has_info':fields.boolean('Has info?'),
        'launchpad': fields.char('Launchpad branch', size=256),
    }
    
    def onchange_module_id(self, cr, uid, ids, module_id, context={}):
        
        module = self.pool.get('ir.module.module').browse(cr, uid, module_id, context=context)
        name = module.name + '_doc'
        
        return {'value': {'name': name}}


class ir_module_module(orm.Model):
    
    _inherit = 'ir.module.module'
    
    _columns = {
        'doc_id': fields.many2one('module.doc', 'Extra documentation'),
        'ext_desc_html': fields.related('doc_id',
                                        'ext_desc_html',
                                        type="html",
                                        string="Extended description (HTML)",
                                        store=False),
    }
