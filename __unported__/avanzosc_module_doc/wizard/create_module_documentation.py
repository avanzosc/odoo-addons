# -*- encoding: utf-8 -*-
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
from openerp.tools.translate import _


class create_extra_documentation(orm.TransientModel):
    _name = 'module.doc.create'

    def create_documentation(self, cr, uid, ids, context=None):
        doc_obj = self.pool.get('module.doc')
        mod_obj = self.pool.get('ir.module.module')
        for id in ids:
            search_ids = doc_obj.search(cr, uid, [('module_id', '=', id)],
                                        context=context)
            if not search_ids:
                created_id = doc_obj.create(cr, uid, {'module_id': id},
                                            context=context)
                name = doc_obj.onchange_module_id(cr, uid, [created_id], id,
                                                  context=context)['value']['name']
                doc_obj.write(cr, uid, created_id, {'name': name},
                              context=context)
                mod_obj.write(cr, uid, id, {'doc_id': created_id},
                              context=context)
            else:
                for search_id in search_ids:
                    doc_obj.write(cr, uid, search_id, {'has_info': True},
                                  context=context)
                    mod_obj.write(cr, uid, id, {'doc_id': search_id},
                                  context=context)
        return {
            'name': _('Extra documentation'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'module.doc',
            'type': 'ir.actions.act_window',
        }

    def create_documentation_all(self, cr, uid, ids, context):
        mod_obj = self.pool.get('ir.module.module')
        all_ids = mod_obj.search(cr, uid, [])
        return self.create_documentation(cr, uid, all_ids, context)

    def create_documentation_installed(self, cr, uid, ids, context):
        mod_obj = self.pool.get('ir.module.module')
        installed_ids = mod_obj.search(cr, uid, [('state', '=', 'installed')])
        return self.create_documentation(cr, uid, installed_ids, context)
