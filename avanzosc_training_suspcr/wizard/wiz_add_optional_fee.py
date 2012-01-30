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

class wiz_add_optional_fee(osv.osv_memory):
    _name = 'wiz.add.optional.fee'
    _description = 'Wizard to add optional fee'
 
    _columns = {
        'fee_list': fields.one2many('wiz.training.fee.master', 'wiz_id', 'List of Fee'),
        'recog_list': fields.one2many('wiz.training.recog.master', 'wiz_id', 'List of Recognition'),
    }
    
    def default_get(self, cr, uid, fields_list, context=None):
        values = {}
        fee_items = []
        recog_items = []
        fee_master_obj = self.pool.get('training.fee.master')
        recog_master_obj = self.pool.get('training.recog.master')
        fee_master_ids = fee_master_obj.search(cr, uid, [])
        recog_master_ids = recog_master_obj.search(cr, uid, [])
        
        
        for fee in self.browse(cr, uid, fee_master_ids):
            fee_items.append({
                'name': fee.name,
                'value': fee.value,
                'wiz_id': 1,
            })
            
        for recog in self.browse(cr, uid, recog_master_ids):
            recog_items.append({
                'name': recog.name,
                'value': recog.value,
                'wiz_id': 1,
            })
            
        values = {
            'fee_list': fee_items,
            'recog_list': recog_items,
        }
        return values
    
wiz_add_optional_fee()

class wiz_training_fee_master(osv.osv_memory):
    _name = 'wiz.training.fee.master'
    _description = 'Fee Wizard List'
 
    _columns = {
            'name': fields.char('Description', size=64),
            'value': fields.float('Value'),
            'check': fields.boolean('Check'),
            'wiz_id': fields.many2one('wiz.add.optional.fee', 'Wizard', required=True),
        }
wiz_training_fee_master()

class wiz_training_recog_master(osv.osv_memory):
    _name = 'wiz.training.recog.master'
    _description = 'Recognition Wizard List'
 
    _columns = {
            'name': fields.char('Description', size=64),
            'value': fields.float('Value'),
            'check': fields.boolean('Check'),
            'wiz_id': fields.many2one('wiz.add.optional.fee', 'Wizard', required=True),
        }
wiz_training_recog_master()