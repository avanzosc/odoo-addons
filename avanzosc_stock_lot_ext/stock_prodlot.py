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

class stock_production_lot_explot(osv.osv):

    _name = 'stock.production.lot.explot'
    _description = 'Explotation Type'
 
    _columns = {
            'name':fields.char('Code', size=1, required=True),
            'descript':fields.char('Name', size=64),
    }
    
    def name_get(self, cr, uid, ids, context=None):
        res = []
        result = self.read(cr, uid, ids, ['name'], context)
        for code in result:
            res.append((code.values()[1], code.values()[0]))
        return res
    
stock_production_lot_explot()

class stock_production_lot_color(osv.osv):

    _name = 'stock.production.lot.color'
    _description = 'Chicken Color'
 
    _columns = {
             'name':fields.char('Code', size=1, required=True),
             'descript':fields.char('Name', size=64),
    }
    
    
    def name_get(self, cr, uid, ids, context=None):
        res = []
        result = self.read(cr, uid, ids, ['name'], context)
        for code in result:
            res.append((code.values()[1], code.values()[0]))
        return res
    
stock_production_lot_color()

class stock_production_lot(osv.osv):

    _inherit = 'stock.production.lot'
 
    _columns = {
            'explotation':fields.many2one('stock.production.lot.explot', 'Explotation type'),
            'color':fields.many2one('stock.production.lot.color', 'Color'),
            'weight': fields.float('Weight'),
    }
stock_production_lot()

class split_in_production_lot(osv.osv_memory):
    _inherit = "stock.move.split"
    
    def split_lot(self, cr, uid, ids, context=None):
        values = {}
        stock_move_obj = self.pool.get('stock.move')
        prodlot_obj = self.pool.get('stock.production.lot')
        super(split_in_production_lot, self).split_lot(cr, uid, ids, context)
        for wizard in self.browse(cr, uid, ids):
            for line in wizard.line_ids:
                for move in stock_move_obj.browse(cr, uid, context.get('active_ids')):
                    if line.explotation and line.name == move.prodlot_id.name:
                        values = {
                            'explotation': line.explotation.id,
                        }
                    if line.color and line.name == move.prodlot_id.name:
                        values.update({
                            'color': line.color.id,
                        })
                    prodlot_obj.write(cr, uid, move.prodlot_id.id, values)
        return {'type': 'ir.actions.act_window_close'}
    
split_in_production_lot()

class stock_move_split_lines(osv.osv_memory):
    _inherit= "stock.move.split.lines"
    
    _columns = {
            'explotation':fields.many2one('stock.production.lot.explot', 'Explotation type'),
            'color':fields.many2one('stock.production.lot.color', 'Color'),
    }
stock_move_split_lines()
