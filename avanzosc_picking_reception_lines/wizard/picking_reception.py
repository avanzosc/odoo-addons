# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011-2012 Daniel (Avanzosc) <http://www.avanzosc.com>
#    14/11/2011
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the  GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from tools.translate import _
import time

class stock_partial_move(osv.osv_memory):
    
    _description = 'stock partial move Inheritance'
    _inherit = 'stock.partial.move'
    _columns = {
                'supplierref':fields.char('Supplier Ref.', size=34),            
        }
    
    
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        
        move_ids =  context.get('active_ids', False)
        if move_ids:
            move_obj = self.pool.get('stock.move').browse(cr,uid,move_ids)
            partner = move_obj[0].partner_id.id
            for move_id in move_obj:
                if (move_id.partner_id.id != partner ):
                    raise osv.except_osv(_('Error!'), _('The selected lines must have the same partner.')) 
        result = super(stock_partial_move,self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
        move_ids = context.get('active_ids', False)    
        message = {
                'title' : _('Deliver Products'),
                'info' : _('Delivery Information'),
                'button' : _('Deliver'),
                }
        if context:            
            if context.get('product_receive', False):
                message = {
                    'title' : _('Receive Products'),
                    'info' : _('Receive Information'),
                    'button' : _('Receive'),
                } 
        message['picking_type'] = self.__get_picking_type(cr, uid, move_ids)
        _moves_arch_lst ="""
                <form string="%(title)s">
                    <separator colspan="4" string="%(info)s"/>
                    <field name="date" colspan="2"/>
                    <field name="supplierref" colspan="2"/>
                    <separator colspan="4" string="Move Detail"/>
                    <field name="%(picking_type)s" colspan="4" nolabel="1" mode="tree,form" width="550" height="200" ></field>      
                    <separator string="" colspan="4" />
                    <label string="" colspan="2"/>
                    <group col="2" colspan="2">
                        <button icon='gtk-cancel' special="cancel" string="_Cancel" />
                        <button name="do_partial" string="%(button)s"
                            colspan="1" type="object" icon="gtk-apply" />
                    </group>
                </form> """  % message
        result['arch'] = _moves_arch_lst
        return result
        
    def do_partial(self, cr, uid, ids, context=None):
        
        super (stock_partial_move,self).do_partial(cr, uid, ids, context)  
        if context is None:
            context = {}
        move_objs = self.pool.get('stock.move')
        move_ids = context.get('active_ids', False)
        pickings = self.pool.get('stock.picking')
        partner=False
        pick_list =[] # stock picking id list
        for pick_line in move_ids: # Picking_list of the lines to be moved
            stock_pick = move_objs.browse(cr, uid, pick_line).picking_id # Movement Stock_picking 
            if not partner:
                partner = stock_pick.partner_id.id
            if pick_list.count(stock_pick.id) == 0 :
                pick_list.append(stock_pick.id)
        address = self.pool.get('res.partner.address').search(cr,uid,[('partner_id','=',partner)])
        ref = self.browse(cr,uid,ids[0]).supplierref
        new_pick_id = False 
        origin = ''
        purch_ori = False
        for picking in pick_list:
            pick_for_list = pick_list[:]
            move_lines = {}
            move_lines = move_objs.search(cr,uid,[('picking_id', '=', picking)]) #Product Stock move lines
            pick_moveline_list = move_lines[:]
            current_picking = pickings.browse(cr,uid,picking)
            move_lines_for = move_lines[:]
            lines_for_assign = []
            for line in move_lines_for: # Clean assigned lines
                line_obj= move_objs.browse(cr,uid,line)
                estado = line_obj.state
                if line_obj.state == 'assigned' :
                    lines_for_assign.append(line)
                    move_lines.remove (line)
            if move_lines != []:
                origin_picking_add = False # Origin data not defined
                for m_line in move_lines:
                    pick_moveline_list.remove(m_line)
                    if pick_moveline_list != []: # all moved lines add to the new picking
                        if not new_pick_id: #new picking does not exist
                            new_pick_id = pickings.create(cr, uid, {'type':'in'}) # Create New Picking
                            new_picking = pickings.browse(cr,uid,new_pick_id)
                            origin_picking = False
                        move_objs.write(cr, uid, m_line, {'picking_id': new_pick_id})
                        if not origin_picking_add: # Picking Origin data
                            if not origin_picking : # if first picking do
                                purch_ori = current_picking.origin
                                origin_picking = True
                            else : # add the rest picking origins
                                purch_ori= purch_ori + ' | ' + current_picking.origin
                            origin_picking_add = True
                            pickings.write(cr, uid, new_pick_id,{'origin':purch_ori, 'address_id': address[0]}) #Origin defined
                        pickings.write(cr, uid, picking, {'backorder_id': new_pick_id})
                        if ref:
                            pickings.write(cr, uid, new_pick_id, {'supplierpack': ref})
                    else:  # moved lines finish the stock picking
                        if ref:
                            pickings.write(cr, uid,picking , {'supplierpack': ref, 'state' : 'done'})
        return {}


stock_partial_move()
