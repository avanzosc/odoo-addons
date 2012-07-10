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

from osv import fields
from osv import osv
from tools import config

import netsvc
import time
from mx import DateTime
from tools.translate import _
import math
import decimal_precision as dp
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class procurement_order(osv.osv):
    _inherit = 'procurement.order'
    _columns = {
        'maker_id':fields.many2one('mrp.maker', 'Config.'),
        'size_x': fields.float('Width'),
        'size_y': fields.float('Length'),
        'size_z': fields.float('Thickness'),
        'density': fields.float('Density', help='Density unit= (uom of weight/(uom of size)^3)'),
        'shape' : fields.selection([('quadrangular', 'Quadrangular'), ('cylindrical', 'Cylindrical'), ('other', 'Other')], 'Shape', help="Weight Formula for Quadrangular = width*length*thickness*density \n Weight Formula for Cylindrical= (diameter/2)^2*pi*thickness*density"),
        'diameter' : fields.float('Diameter'),
        'weight': fields.float('Weight'),
        'price_type': fields.selection((('weight', 'Weight'), ('units', 'Units')), 'Purchase price in', help="United of measure for purchase operations"),
    }
    
    def make_po(self, cr, uid, ids, context=None):
        """ Make purchase order from procurement
        @return: New created Purchase Orders procurement wise
        """
        res = {}
        if context is None:
            context = {}
        company = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id
        partner_obj = self.pool.get('res.partner')
        uom_obj = self.pool.get('product.uom')
        pricelist_obj = self.pool.get('product.pricelist')
        prod_obj = self.pool.get('product.product')
        acc_pos_obj = self.pool.get('account.fiscal.position')
        po_obj = self.pool.get('purchase.order')
        po_line_obj = self.pool.get('purchase.order.line')
        for procurement in self.browse(cr, uid, ids, context=context):
            res_id = procurement.move_id.id
            partner = procurement.product_id.seller_id # Taken Main Supplier of Product of Procurement.
            seller_qty = procurement.product_id.seller_qty
            seller_delay = int(procurement.product_id.seller_delay)
            partner_id = partner.id
            address_id = partner_obj.address_get(cr, uid, [partner_id], ['delivery'])['delivery']
            pricelist_id = partner.property_product_pricelist_purchase.id
            fiscal_position = partner.property_account_position and partner.property_account_position.id or False

            uom_id = procurement.product_id.uom_po_id.id

            qty = uom_obj._compute_qty(cr, uid, procurement.product_uom.id, procurement.product_qty, uom_id)
            if seller_qty:
                qty = max(qty,seller_qty)

            price = pricelist_obj.price_get(cr, uid, [pricelist_id], procurement.product_id.id, qty, partner_id, {'uom': uom_id})[pricelist_id]

            newdate = datetime.strptime(procurement.date_planned, '%Y-%m-%d %H:%M:%S')
            newdate = (newdate - relativedelta(days=company.po_lead)) - relativedelta(days=seller_delay)

            res_onchange = po_line_obj.product_id_change(cr, uid, ids, pricelist_id, procurement.product_id.id, qty, uom_id,
                partner_id, time.strftime('%Y-%m-%d'), fiscal_position=fiscal_position, date_planned=datetime.now() + relativedelta(days=seller_delay or 0.0),
            name=procurement.name, price_unit=procurement.product_id.list_price, notes=procurement.product_id.description_purchase)

            #Passing partner_id to context for purchase order line integrity of Line name
            context.update({'lang': partner.lang, 'partner_id': partner_id})

            product = prod_obj.browse(cr, uid, procurement.product_id.id, context=context)

            line = {
                'name': product.partner_ref,
                'product_qty': res_onchange['value']['product_qty'],
                'product_id': procurement.product_id.id,
                'size_x':procurement.size_x,
                'size_y':procurement.size_y,
                'size_z':procurement.size_z,
                'density':procurement.density,
                'shape':procurement.shape,
                'purchase_price':procurement.price_type,
                'diameter':procurement.diameter,
                'weight': procurement.weight,
                'product_uom': res_onchange['value']['product_uom'],
                'price_unit': res_onchange['value']['price_unit'],
                'date_planned': newdate.strftime('%Y-%m-%d %H:%M:%S'),
                'move_dest_id': res_id,
                'notes': product.description_purchase,
            }

            taxes_ids = procurement.product_id.product_tmpl_id.supplier_taxes_id
            taxes = acc_pos_obj.map_tax(cr, uid, partner.property_account_position, taxes_ids)
            line.update({
                'taxes_id': [(6,0,taxes)]
            })
            purchase_id = po_obj.create(cr, uid, {
                'origin': procurement.origin,
                'partner_id': partner_id,
                'partner_address_id': address_id,
                'location_id': procurement.location_id.id,
                'pricelist_id': pricelist_id,
                'order_line': [(0,0,line)],
                'company_id': procurement.company_id.id,
                'fiscal_position': partner.property_account_position and partner.property_account_position.id or False
            })
            res[procurement.id] = purchase_id
            self.write(cr, uid, [procurement.id], {'state': 'running', 'purchase_id': purchase_id})
        return res
    
    
    def make_mo(self, cr, uid, ids, context=None):
        """ Make Manufacturing(production) order from procurement
        @return: New created Production Orders procurement wise 
        """
        res = {}
        company = self.pool.get('res.users').browse(cr, uid, uid, context).company_id
        production_obj = self.pool.get('mrp.production')
        move_obj = self.pool.get('stock.move')
        lot_obj = self.pool.get('stock.production.lot')
        pl_obj = self.pool.get('mrp.production.product.line')
        wf_service = netsvc.LocalService("workflow")
        procurement_obj = self.pool.get('procurement.order')
        for procurement in procurement_obj.browse(cr, uid, ids, context=context):
            res_id = procurement.move_id.id
            loc_id = procurement.location_id.id
            newdate = datetime.strptime(procurement.date_planned, '%Y-%m-%d %H:%M:%S') - relativedelta(days=procurement.product_id.product_tmpl_id.produce_delay or 0.0)
            newdate = newdate - relativedelta(days=company.manufacturing_lead)
            if procurement.maker_id:
                res_list = []  
                for f_line in procurement.maker_id.final_line_ids:
                    val_fl = {
                       'product_id':f_line.product_id.id,
                       'product_qty':f_line.product_qty,
                       'product_uom':f_line.product_uom.id,
                       'shape':f_line.shape,
                       'size_x':f_line.size_x,
                       'size_y':f_line.size_y,
                       'size_z':f_line.size_z,
                       'diameter':f_line.diameter,
                       'weight':f_line.weight,
                       'density':f_line.density,
                       }
                    val_lot = {
                       'product_id':f_line.product_id.id,
                       'shape':f_line.shape,
                       'size_x':f_line.size_x,
                       'size_y':f_line.size_y,
                       'size_z':f_line.size_z,
                       'diameter':f_line.diameter,
                       'weight':f_line.weight,
                       'density':f_line.density,
                       }
                    source = procurement.maker_id.product_id.product_tmpl_id.property_stock_production.id
                    dest = procurement.location_id.id
                    lot_o = False
                    lot_domain = [('product_id', '=', f_line.product_id.id),('shape', '=', f_line.shape),('size_x', '=', f_line.size_x),('size_y', '=', f_line.size_y),('size_z','=', f_line.size_z),('diameter', '=', f_line.diameter),('weight', '=', f_line.weight),('density', '=', f_line.density)]
                    lot = lot_obj.search(cr,uid,lot_domain)
                    if lot:
                       lot_o=lot[0]
                    else:
                        lot_o = lot_obj.create(cr,uid,val_lot)
                        lot_obj.generate_serial(cr,uid,[lot_o]) 
                    val_fl.update({'name':f_line.product_id.name, 'location_id':source, 'location_dest_id':dest, 'prodlot_id':lot_o})
                    pc_id = move_obj.create(cr,uid,val_fl)
                    res_list.append(pc_id)
                produce_id = production_obj.create(cr, uid, {
                    'origin': procurement.origin,
                    'product_id': procurement.maker_id.product_id.id,
                    'product_qty': procurement.maker_id.product_qty,
                    'product_uom': procurement.maker_id.product_uom.id,
                    'product_uos_qty': procurement.product_uos and procurement.product_uos_qty or False,
                    'product_uos': procurement.product_uos and procurement.product_uos.id or False,
                    'location_src_id': procurement.location_id.id,
                    'location_dest_id': procurement.location_id.id,
                    'bom_id': procurement.bom_id and procurement.bom_id.id or False,
                    'date_planned': newdate.strftime('%Y-%m-%d %H:%M:%S'),
                    'move_prod_id': res_id,
                    'company_id': procurement.company_id.id,
                    'move_created_ids': [(6, 0, res_list)],
                    'shape':procurement.maker_id.shape,
                    'size_x':procurement.maker_id.size_x,
                    'size_y':procurement.maker_id.size_y,
                    'size_z':procurement.maker_id.size_z,
                    'diameter':procurement.maker_id.diameter,
                    'weight':procurement.maker_id.weight,
                    'density':procurement.maker_id.density,
                    'maker':procurement.maker_id.id,
                })
                
                for line in procurement.maker_id.line_ids:
                    val_l = {
                       'product_id':line.product_id.id,
                       'product_qty':line.product_qty,
                       'product_uom':line.product_uom.id,
                       'shape':line.shape,
                       'size_x':line.size_x,
                       'size_y':line.size_y,
                       'size_z':line.size_z,
                       'diameter':line.diameter,
                       'weight':line.weight,
                       'density':line.density,
                       }
                    val_l.update({'production_id':produce_id, 'name':line.product_id.name})
                    pl_obj.create(cr,uid,val_l)
                res[procurement.id] = produce_id
                self.write(cr, uid, [procurement.id], {'state': 'running'})
            else:
                produce_id = production_obj.create(cr, uid, {
                    'origin': procurement.origin,
                    'product_id': procurement.product_id.id,
                    'product_qty': procurement.product_qty,
                    'product_uom': procurement.product_uom.id,
                    'product_uos_qty': procurement.product_uos and procurement.product_uos_qty or False,
                    'product_uos': procurement.product_uos and procurement.product_uos.id or False,
                    'location_src_id': procurement.location_id.id,
                    'location_dest_id': procurement.location_id.id,
                    'bom_id': procurement.bom_id and procurement.bom_id.id or False,
                    'date_planned': newdate.strftime('%Y-%m-%d %H:%M:%S'),
                    'move_prod_id': res_id,
                    'company_id': procurement.company_id.id,
                })
                res[procurement.id] = produce_id
                self.write(cr, uid, [procurement.id], {'state': 'running'})
                bom_result = production_obj.action_compute(cr, uid,
                        [produce_id], properties=[x.id for x in procurement.property_ids])
                wf_service.trg_validate(uid, 'mrp.production', produce_id, 'button_confirm', cr)
                move_obj.write(cr, uid, [res_id],
                        {'location_id': procurement.location_id.id})
        return res
procurement_order()

class make_procurement(osv.osv_memory):
    _inherit = 'make.procurement'
    
    def make_procurement(self, cr, uid, ids, context=None):
        """ Creates procurement order for selected product.
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: List of IDs selected
        @param context: A standard dictionary
        @return: A dictionary which loads Procurement form view.
        """
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context).login
        wh_obj = self.pool.get('stock.warehouse')
        procurement_obj = self.pool.get('procurement.order')
        wf_service = netsvc.LocalService("workflow")
        data_obj = self.pool.get('ir.model.data')

        for proc in self.browse(cr, uid, ids, context=context):
            wh = wh_obj.browse(cr, uid, proc.warehouse_id.id, context=context)
            procure_id = procurement_obj.create(cr, uid, {
                'name':'INT: '+str(user),
                'date_planned': proc.date_planned,
                'product_id': proc.product_id.id,
                'product_qty': proc.qty,
                'product_uom': proc.uom_id.id,
                'location_id': wh.lot_stock_id.id,
                'procure_method':'make_to_order',
            })

            wf_service.trg_validate(uid, 'procurement.order', procure_id, 'button_confirm', cr)


        id2 = data_obj._get_id(cr, uid, 'procurement', 'procurement_tree_view')
        id3 = data_obj._get_id(cr, uid, 'procurement', 'procurement_form_view')

        if id2:
            id2 = data_obj.browse(cr, uid, id2, context=context).res_id
        if id3:
            id3 = data_obj.browse(cr, uid, id3, context=context).res_id

        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'procurement.order',
            'res_id' : procure_id,
            'views': [(id3,'form'),(id2,'tree')],
            'type': 'ir.actions.act_window',
         }
make_procurement()