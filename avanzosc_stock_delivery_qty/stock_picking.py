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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

from osv import osv, fields
from tools.translate import _

import decimal_precision as dp
import netsvc


class account_invoice_line(osv.osv):
    _inherit = 'account.invoice.line'
    _columns={
              'picking_qty': fields.float('Picking qty', readonly=True),
              'sup_picking_ref':fields.char('Sup. Picking ref',size=34, readonly=True),
              }
account_invoice_line()

class account_invoice(osv.osv):
    _inherit = "account.invoice"
    
    def _calculate_total_invoice(self, cr, uid, ids, field_name, arg, context=None):
        qty = 0.0
        res={}
        inv = self.pool.get('account.invoice').browse(cr,uid,ids)[0]
        for line in inv.invoice_line:            
            qty = qty + line.quantity
        res[inv.id] = qty
        return res
    
    def _calculate_total_picking(self, cr, uid, ids, field_name, arg, context=None):
        qty = 0.0
        res={}
        inv = self.pool.get('account.invoice').browse(cr,uid,ids)[0]
        for line in inv.invoice_line:            
            qty = qty + line.picking_qty
        res[inv.id] = qty
        return res
    
    _columns = {
                'total_invoice_qty':fields.function(_calculate_total_invoice,  method=True, type='float', string="Total invoice qty", store=True),
                'total_pick_qty':fields.function(_calculate_total_picking,  method=True, type='float', string="Total picking qty", store=True),
                }
    
    
account_invoice()
class stock_move(osv.osv):
    _inherit = 'stock.move'
    
    _columns = {                
                'product_qty':fields.float('Move Qty', digits_compute=dp.get_precision('Product UoM'), required=True,states={'done': [('readonly', True)]}),
                'sup_qty':fields.float('Order Qty', digits_compute=dp.get_precision('Product UoM'), readonly=True),
                'invoice_qty':fields.float('Invoice Qty', digits_compute=dp.get_precision('Product UoM'), states={'done': [('readonly', True)]})
                }
    
    
    def onchange_qty(self, cr, uid, fields, product_qty, context=None):
        res = {}
        if product_qty:
            res = {
                'invoice_qty': product_qty,            
                }
        return {'value': res}
    
stock_move()

class purchase_order(osv.osv):
    _inherit = 'purchase.order'
    
    def action_picking_create(self,cr, uid, ids, *args):        
        lines = self.pool.get('stock.move')        
        pick_id = super(purchase_order, self).action_picking_create(cr, uid, ids)
        ids = lines.search(cr, uid,[('picking_id','=',pick_id)])
        for line_id in ids:
            line_obj = lines.browse(cr, uid, line_id)
            qty = line_obj.product_qty
            lines.write(cr, uid, [line_id], {'sup_qty':qty, 'invoice_qty':qty, 'product_qty':qty})
        return pick_id
    
purchase_order()

class sale_order(osv.osv):
    _inherit = 'sale.order'
    
    def action_ship_create(self, cr, uid, ids, *args):
        wf_service = netsvc.LocalService("workflow")
        picking_id = False
        move_obj = self.pool.get('stock.move')
        proc_obj = self.pool.get('procurement.order')
        company = self.pool.get('res.users').browse(cr, uid, uid).company_id
        for order in self.browse(cr, uid, ids, context={}):
            proc_ids = []
            output_id = order.shop_id.warehouse_id.lot_output_id.id
            picking_id = False
            for line in order.order_line:
                proc_id = False
                date_planned = datetime.now() + relativedelta(days=line.delay or 0.0)
                date_planned = (date_planned - timedelta(days=company.security_lead)).strftime('%Y-%m-%d %H:%M:%S')

                if line.state == 'done':
                    continue
                move_id = False
                if line.product_id and line.product_id.product_tmpl_id.type in ('product', 'consu'):
                    location_id = order.shop_id.warehouse_id.lot_stock_id.id
                    if not picking_id:
                        pick_name = self.pool.get('ir.sequence').get(cr, uid, 'stock.picking.out')
                        picking_id = self.pool.get('stock.picking').create(cr, uid, {
                            'name': pick_name,
                            'origin': order.name,
                            'type': 'out',
                            'state': 'auto',
                            'move_type': order.picking_policy,
                            'sale_id': order.id,
                            'address_id': order.partner_shipping_id.id,
                            'note': order.note,
                            'invoice_state': (order.order_policy=='picking' and '2binvoiced') or 'none',
                            'company_id': order.company_id.id,
                        })
                    move_id = self.pool.get('stock.move').create(cr, uid, {
                        'name': line.name[:64],
                        'picking_id': picking_id,
                        'product_id': line.product_id.id,
                        'date': date_planned,
                        'date_expected': date_planned,
                        'product_qty': line.product_uom_qty,
                        'sup_qty' : line.product_uom_qty,
                        'invoice_qty' : line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'product_uos_qty': line.product_uos_qty,
                        'product_uos': (line.product_uos and line.product_uos.id)\
                                or line.product_uom.id,
                        'product_packaging': line.product_packaging.id,
                        'address_id': line.address_allotment_id.id or order.partner_shipping_id.id,
                        'location_id': location_id,
                        'location_dest_id': output_id,
                        'sale_line_id': line.id,
                        'tracking_id': False,
                        'state': 'draft',
                        #'state': 'waiting',
                        'note': line.notes,
                        'company_id': order.company_id.id,
                    })

                if line.product_id:
                    proc_id = self.pool.get('procurement.order').create(cr, uid, {
                        'name': line.name,
                        'origin': order.name,
                        'date_planned': date_planned,
                        'product_id': line.product_id.id,
                        'product_qty': line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'product_uos_qty': (line.product_uos and line.product_uos_qty)\
                                or line.product_uom_qty,
                        'product_uos': (line.product_uos and line.product_uos.id)\
                                or line.product_uom.id,
                        'location_id': order.shop_id.warehouse_id.lot_stock_id.id,
                        'procure_method': line.type,
                        'move_id': move_id,
                        'property_ids': [(6, 0, [x.id for x in line.property_ids])],
                        'company_id': order.company_id.id,
                    })
                    proc_ids.append(proc_id)
                    self.pool.get('sale.order.line').write(cr, uid, [line.id], {'procurement_id': proc_id})
                    if order.state == 'shipping_except':
                        for pick in order.picking_ids:
                            for move in pick.move_lines:
                                if move.state == 'cancel':
                                    mov_ids = move_obj.search(cr, uid, [('state', '=', 'cancel'),('sale_line_id', '=', line.id),('picking_id', '=', pick.id)])
                                    if mov_ids:
                                        for mov in move_obj.browse(cr, uid, mov_ids):
                                            move_obj.write(cr, uid, [move_id], {'product_qty': mov.product_qty, 'product_uos_qty': mov.product_uos_qty})
                                            proc_obj.write(cr, uid, [proc_id], {'product_qty': mov.product_qty, 'product_uos_qty': mov.product_uos_qty})

            val = {}

            if picking_id:
                wf_service.trg_validate(uid, 'stock.picking', picking_id, 'button_confirm', cr)

            for proc_id in proc_ids:
                wf_service.trg_validate(uid, 'procurement.order', proc_id, 'button_confirm', cr)

            if order.state == 'shipping_except':
                val['state'] = 'progress'
                val['shipped'] = False

                if (order.order_policy == 'manual'):
                    for line in order.order_line:
                        if (not line.invoiced) and (line.state not in ('cancel', 'draft')):
                            val['state'] = 'manual'
                            break
            self.write(cr, uid, [order.id], val)
        return True
sale_order()

class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    
    def _calculate_total_invoice(self, cr, uid, ids, field_name, arg, context=None):
        qty = 0.0
        res={}
        pick = self.pool.get('stock.picking').browse(cr,uid,ids)[0]
        for line in pick.move_lines:            
            qty = qty + line.invoice_qty
        res[pick.id] = qty
        return res
    
    def _calculate_total_picking(self, cr, uid, ids, field_name, arg, context=None):
        qty = 0.0
        res={}
        pick = self.pool.get('stock.picking').browse(cr,uid,ids)[0]
        for line in pick.move_lines:            
            qty = qty + line.product_qty
        res[pick.id] = qty
        return res
    
    _columns = {
                'total_invoice_qty': fields.function(_calculate_total_invoice,  method=True, type='float', string="Total invoice qty", store=True),
                'total_picking_qty': fields.function(_calculate_total_picking,  method=True, type='float', string="Total picking qty", store=True),
                'manual_pick_ref':fields.char('Manual picking ref.', size=80, required = True),
                'min_date_editable': fields.datetime('Expected Date', help="Expected date for the picking to be processed"),
    }
    
    def default_get(self, cr, uid, fields_list, context=None):
        values = super(stock_picking, self).default_get(cr, uid, fields_list, context)
        if 'date' in values:
            values.update({
                'min_date_editable': values['date'],
            })
        return values
    
    def action_invoice_create(self, cr, uid, ids, journal_id=False,
            group=False, type='out_invoice', context=None):
        """ Creates invoice based on the invoice state selected for picking.
        @param journal_id: Id of journal
        @param group: Whether to create a group invoice or not
        @param type: Type invoice to be created
        @return: Ids of created invoices for the pickings
        """
        if context is None:
            context = {}

        invoice_obj = self.pool.get('account.invoice')
        invoice_line_obj = self.pool.get('account.invoice.line')
        address_obj = self.pool.get('res.partner.address')
        invoices_group = {}
        res = {}
        inv_type = type
        for picking in self.browse(cr, uid, ids, context=context):
            if picking.invoice_state != '2binvoiced':
                continue
            payment_term_id = False
            partner =  picking.address_id and picking.address_id.partner_id
            if not partner:
                raise osv.except_osv(_('Error, no partner !'),
                    _('Please put a partner on the picking list if you want to generate invoice.'))

            if not inv_type:
                inv_type = self._get_invoice_type(picking)

            if inv_type in ('out_invoice', 'out_refund'):
                account_id = partner.property_account_receivable.id
                payment_term_id = self._get_payment_term(cr, uid, picking)
            else:
                account_id = partner.property_account_payable.id

            address_contact_id, address_invoice_id = \
                    self._get_address_invoice(cr, uid, picking).values()
            address = address_obj.browse(cr, uid, address_contact_id, context=context)

            comment = self._get_comment_invoice(cr, uid, picking)
            comment = comment
            if group and partner.id in invoices_group:
                invoice_id = invoices_group[partner.id]
                invoice = invoice_obj.browse(cr, uid, invoice_id)
                invoice_vals = {
                    'name': (invoice.name or '') + ', ' + (picking.name or ''),
                    'origin': (invoice.origin or '') + ', ' + (picking.name or '') + (picking.origin and (':' + picking.origin) or '') + ((':' + picking.manual_pick_ref) or ''),
                    'comment': (comment and (invoice.comment and invoice.comment+"\n"+comment or comment)) or (invoice.comment and invoice.comment or ''),
                    'date_invoice':context.get('date_inv',False),
                    'user_id':uid
                }
                invoice_obj.write(cr, uid, [invoice_id], invoice_vals, context=context)
            else:
                if picking.manual_pick_ref == False:
                    manpicref = ''
                else: manpicref = picking.manual_pick_ref
                invoice_vals = {
                    'name': picking.name,
                    'origin': (picking.name or '') + (picking.origin and (':' + picking.origin) or '') + ((':' + manpicref) or ''),
                    'type': inv_type,
                    'account_id': account_id,
                    'partner_id': address.partner_id.id,
                    'address_invoice_id': address_invoice_id,
                    'address_contact_id': address_contact_id,
                    'comment': comment,
                    'payment_term': payment_term_id,
                    'fiscal_position': partner.property_account_position.id,
                    'date_invoice': context.get('date_inv',False),
                    'company_id': picking.company_id.id,
                    'user_id':uid
                }
                cur_id = self.get_currency_id(cr, uid, picking)
                if cur_id:
                    invoice_vals['currency_id'] = cur_id
                if journal_id:
                    invoice_vals['journal_id'] = journal_id
                invoice_id = invoice_obj.create(cr, uid, invoice_vals,
                        context=context)
                invoices_group[partner.id] = invoice_id
            res[picking.id] = invoice_id
            total = 0
            egg_kop = 0
            note = None
            for move_line in picking.move_lines:
                if move_line.state == 'cancel':
                    continue
                origin = move_line.picking_id.name or ''
                if move_line.picking_id.origin:
                    origin += ':' + move_line.picking_id.origin
                if group:
                    name = (picking.name or '') + '-' + move_line.name
                else:
                    name = move_line.name

                if inv_type in ('out_invoice', 'out_refund'):
                    account_id = move_line.product_id.product_tmpl_id.\
                            property_account_income.id
                    if not account_id:
                        account_id = move_line.product_id.categ_id.\
                                property_account_income_categ.id
                else:
                    account_id = move_line.product_id.product_tmpl_id.\
                            property_account_expense.id
                    if not account_id:
                        account_id = move_line.product_id.categ_id.\
                                property_account_expense_categ.id

                price_unit = self._get_price_unit_invoice(cr, uid,
                        move_line, inv_type)
                discount = self._get_discount_invoice(cr, uid, move_line)
                tax_ids = self._get_taxes_invoice(cr, uid, move_line, inv_type)
                account_analytic_id = self._get_account_analytic_invoice(cr, uid, picking, move_line)

                #set UoS if it's a sale and the picking doesn't have one
                uos_id = move_line.product_uos and move_line.product_uos.id or False
                if not uos_id and inv_type in ('out_invoice', 'out_refund'):
                    uos_id = move_line.product_uom.id
                account_id = self.pool.get('account.fiscal.position').map_account(cr, uid, partner.property_account_position, account_id)
                # Codigo Dani
                lote = move_line.prodlot_id
                eggs = self.pool.get('stock.production.lot').browse(cr, uid, lote.id)
                egg_kop = eggs.egg_qty
                invoice_line_list = invoice_line_obj.search(cr,uid,[('invoice_id', '=', invoice_id)])
                if egg_kop > 0:
                    note = _('Número de huevos: ') + str(egg_kop) 
                if invoice_line_list != []:
                    find = False
                    for invo_line in invoice_line_list:
                        invoice_line = invoice_line_obj.browse(cr,uid,invo_line)
                        if invoice_line.product_id.id == move_line.product_id.id:
                            find = True
                            current = invoice_line.quantity + move_line.invoice_qty or move_line.product_uos_qty or move_line.product_qty
                            pick_current = invoice_line.picking_qty + move_line.product_qty
                            egg_tot = invoice_line.note
                            if egg_kop > 0:
                                egg_lag = int(invoice_line.note.lstrip(_('Número de huevos: ')))
                                egg_tot = _('Número de huevos: ') + str(egg_kop + egg_lag) 
                            invoice_line_obj.write(cr, uid, [invo_line],{'quantity': current, 'picking_qty': pick_current, 'note' : egg_tot  })
                   
                    if not find:
                        invoice_line_id = invoice_line_obj.create(cr, uid, {
                        'name': name,
                        'origin': origin,
                        'invoice_id': invoice_id,
                        'uos_id': uos_id,
                        'product_id': move_line.product_id.id,
                        'picking_qty':move_line.product_qty,
                        'sup_picking_ref':picking.supplierpack,
                        'account_id': account_id,
                        'price_unit': price_unit,
                        'discount': discount,
                        'quantity': move_line.invoice_qty or move_line.product_uos_qty or move_line.product_qty,
                        'note' : note,
                        'invoice_line_tax_id': [(6, 0, tax_ids)],
                        'account_analytic_id': account_analytic_id,
                            }, context=context)
                        self._invoice_line_hook(cr, uid, move_line, invoice_line_id)
                else:
                    invoice_line_id = invoice_line_obj.create(cr, uid, {
                    'name': name,
                    'origin': origin,
                    'invoice_id': invoice_id,
                    'uos_id': uos_id,
                    'product_id': move_line.product_id.id,
                    'picking_qty':move_line.product_qty,
                    'sup_picking_ref':picking.supplierpack,
                    'account_id': account_id,
                    'price_unit': price_unit,
                    'discount': discount,
                    'quantity': move_line.invoice_qty or move_line.product_uos_qty or move_line.product_qty,
                    'invoice_line_tax_id': [(6, 0, tax_ids)],
                    'note' : note,
                    'account_analytic_id': account_analytic_id,
                    }, context=context)
                    self._invoice_line_hook(cr, uid, move_line, invoice_line_id)
            # fin codigo Dani
            invoice_obj.button_compute(cr, uid, [invoice_id], context=context,
                    set_total=(inv_type in ('in_invoice', 'in_refund')))
            self.write(cr, uid, [picking.id], {
                'invoice_state': 'invoiced',
                }, context=context)
            self._invoice_hook(cr, uid, picking, invoice_id)
        self.write(cr, uid, res.keys(), {
            'invoice_state': 'invoiced',
            }, context=context)
        return res




    def do_partial(self, cr, uid, ids, partial_datas, context=None):
        """ Makes partial picking and moves done.
        @param partial_datas : Dictionary containing details of partial picking
                          like partner_id, address_id, delivery_date,
                          delivery moves with product_id, product_qty, uom
        @return: Dictionary of values
        """
        if context is None:
            context = {}
        else:
            context = dict(context)
        res = {}
        move_obj = self.pool.get('stock.move')
        product_obj = self.pool.get('product.product')
        currency_obj = self.pool.get('res.currency')
        uom_obj = self.pool.get('product.uom')
        sequence_obj = self.pool.get('ir.sequence')
        wf_service = netsvc.LocalService("workflow")
        for pick in self.browse(cr, uid, ids, context=context):
            new_picking = None
            complete, too_many, too_few = [], [], []
            move_product_qty = {}
            move_invoice_qty = {}
            prodlot_ids = {}
            product_avail = {}
            for move in pick.move_lines:
                if move.state in ('done', 'cancel'):
                    continue
                partial_data = partial_datas.get('move%s'%(move.id), {})
                #Commented in order to process the less number of stock moves from partial picking wizard
                #assert partial_data, _('Missing partial picking data for move #%s') % (move.id)
                product_qty = partial_data.get('product_qty') or 0.0
                invoice_qty = partial_data.get('invoice_qty') or 0.0
                move_product_qty[move.id] = product_qty
                move_invoice_qty[move.id] = invoice_qty
                product_uom = partial_data.get('product_uom') or False
                product_price = partial_data.get('product_price') or 0.0
                product_currency = partial_data.get('product_currency') or False
                prodlot_id = partial_data.get('prodlot_id') or False
                prodlot_ids[move.id] = prodlot_id
                if move.product_qty == product_qty and move.invoice_qty == invoice_qty:
                    complete.append(move)
                elif move.product_qty > product_qty :
                    too_few.append(move)
                else:
                    too_many.append(move)

                # Average price computation
                if (pick.type == 'in') and (move.product_id.cost_method == 'average'):
                    product = product_obj.browse(cr, uid, move.product_id.id)
                    move_currency_id = move.company_id.currency_id.id
                    context['currency_id'] = move_currency_id
                    qty = uom_obj._compute_qty(cr, uid, product_uom, product_qty, product.uom_id.id)

                    if product.id in product_avail:
                        product_avail[product.id] += qty
                    else:
                        product_avail[product.id] = product.qty_available

                    if qty > 0:
                        new_price = currency_obj.compute(cr, uid, product_currency,
                                move_currency_id, product_price)
                        new_price = uom_obj._compute_price(cr, uid, product_uom, new_price,
                                product.uom_id.id)
                        if product.qty_available <= 0:
                            new_std_price = new_price
                        else:
                            # Get the standard price
                            amount_unit = product.price_get('standard_price', context)[product.id]
                            new_std_price = ((amount_unit * product_avail[product.id])\
                                + (new_price * qty))/(product_avail[product.id] + qty)
                        # Write the field according to price type field
                        product_obj.write(cr, uid, [product.id], {'standard_price': new_std_price})

                        # Record the values that were chosen in the wizard, so they can be
                        # used for inventory valuation if real-time valuation is enabled.
                        move_obj.write(cr, uid, [move.id],
                                {'price_unit': product_price,
                                 'price_currency_id': product_currency})


            for move in too_few:
                product_qty = move_product_qty[move.id]
                invoice_qty = move_invoice_qty[move.id]
                
                if not new_picking:
                    new_picking = self.copy(cr, uid, pick.id,
                            {
                                'name': sequence_obj.get(cr, uid, 'stock.picking.%s'%(pick.type)),
                                'move_lines' : [],
                                'state':'draft',
                            })
                if product_qty != 0:
                    defaults = {
                            'product_qty' : product_qty,
                            'invoice_qty' : invoice_qty,
                            'product_uos_qty': product_qty, #TODO: put correct uos_qty
                            'picking_id' : new_picking,
                            'state': 'assigned',
                            'move_dest_id': False,
                            'price_unit': move.price_unit,
                    }
                    prodlot_id = prodlot_ids[move.id]
                    if prodlot_id:
                        defaults.update(prodlot_id=prodlot_id)
                   
                    move_obj.copy(cr, uid, move.id, defaults)
               
                move_obj.write(cr, uid, [move.id],
                        {
                            'product_qty' : move.product_qty - product_qty,
                            'invoice_qty' : move.invoice_qty - invoice_qty,
                            'product_uos_qty':move.product_qty - product_qty, #TODO: put correct uos_qty
                        })

            if new_picking:
                move_obj.write(cr, uid, [c.id for c in complete], {'picking_id': new_picking})
            for move in complete:
                if prodlot_ids.get(move.id):
                    move_obj.write(cr, uid, [move.id], {'prodlot_id': prodlot_ids[move.id]})
            for move in too_many:
                product_qty = move_product_qty[move.id]
                invoice_qty = move_invoice_qty[move.id]
                defaults = {
                    'product_qty' : product_qty,
                    'invoice_qty' : invoice_qty,
                    'product_uos_qty': product_qty, #TODO: put correct uos_qty
                }
                prodlot_id = prodlot_ids.get(move.id)
                if prodlot_ids.get(move.id):
                    defaults.update(prodlot_id=prodlot_id)
                if new_picking:
                    defaults.update(picking_id=new_picking)
                move_obj.write(cr, uid, [move.id], defaults)


            # At first we confirm the new picking (if necessary)
            if new_picking:
                wf_service.trg_validate(uid, 'stock.picking', new_picking, 'button_confirm', cr)
                # Then we finish the good picking
                self.write(cr, uid, [pick.id], {'backorder_id': new_picking})
                self.action_move(cr, uid, [new_picking])
                wf_service.trg_validate(uid, 'stock.picking', new_picking, 'button_done', cr)
                wf_service.trg_write(uid, 'stock.picking', pick.id, cr)
                delivered_pack_id = new_picking
            else:
                self.action_move(cr, uid, [pick.id])
                wf_service.trg_validate(uid, 'stock.picking', pick.id, 'button_done', cr)
                delivered_pack_id = pick.id

            delivered_pack = self.browse(cr, uid, delivered_pack_id, context=context)
            res[pick.id] = {'delivered_picking': delivered_pack.id or False}

        return res

    
stock_picking()

class stock_partial_move_memory_out(osv.osv_memory):
    _inherit = "stock.move.memory.out"
    _columns = {
                'invoice_qty':fields.float('Invoice qty'),
                }
stock_partial_move_memory_out()  
class stock_partial_move_memory_in(osv.osv_memory):
    _inherit = "stock.move.memory.in"
    _columns = {
                'invoice_qty':fields.float('Invoice qty'),
                }
stock_partial_move_memory_in()

class stock_partial_picking(osv.osv_memory):
    _inherit = 'stock.partial.picking'

    def __create_partial_picking_memory(self, move, pick_type):
        move_memory = super(stock_partial_picking, self).__create_partial_picking_memory(move,pick_type)
        move_memory.update({'invoice_qty': move.invoice_qty})
        return move_memory
    
    def do_partial(self, cr, uid, ids, context=None):
        """ Makes partial moves and pickings done.
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param fields: List of fields for which we want default values
        @param context: A standard dictionary
        @return: A dictionary which of fields with values.
        """
        pick_obj = self.pool.get('stock.picking')
        uom_obj = self.pool.get('product.uom')

        picking_ids = context.get('active_ids', False)
        partial = self.browse(cr, uid, ids[0], context=context)
        partial_datas = {
            'delivery_date' : partial.date
        }

        for pick in pick_obj.browse(cr, uid, picking_ids, context=context):
            picking_type = self.get_picking_type(cr, uid, pick, context=context)
            moves_list = picking_type == 'in' and partial.product_moves_in or partial.product_moves_out

            for move in moves_list:

                #Adding a check whether any line has been added with new qty
                if not move.move_id:
                    raise osv.except_osv(_('Processing Error'),\
                    _('You cannot add any new move while validating the picking, rather you can split the lines prior to validation!'))

                calc_qty = uom_obj._compute_qty(cr, uid, move.product_uom.id, \
                                    move.quantity, move.move_id.product_uom.id)
                
                calc_qty2 = uom_obj._compute_qty(cr, uid, move.product_uom.id, \
                                    move.invoice_qty, move.move_id.product_uom.id)
                
                #Adding a check whether any move line contains exceeding qty to original moveline
                
                if calc_qty > move.move_id.product_qty:
                    raise osv.except_osv(_('Processing Error'),
                    _('Processing quantity %d %s for %s is larger than the available quantity %d %s !')\
                    %(move.quantity, move.product_uom.name, move.product_id.name,\
                      move.move_id.product_qty, move.move_id.product_uom.name))

                #Adding a check whether any move line contains qty less than zero
                if calc_qty <= 0:
                    raise osv.except_osv(_('Processing Error'), \
                            _('Can not process quantity %d for Product %s !') \
                            %(move.quantity, move.product_id.name))

                partial_datas['move%s' % (move.move_id.id)] = {
                    'product_id': move.product_id.id,
                    'product_qty': calc_qty,
                    'invoice_qty':calc_qty2,
                    'product_uom': move.move_id.product_uom.id,
                    'prodlot_id': move.prodlot_id.id,
                }
                if (picking_type == 'in') and (move.product_id.cost_method == 'average'):
                    partial_datas['move%s' % (move.move_id.id)].update({
                                                    'product_price' : move.cost,
                                                    'product_currency': move.currency.id,
                                                    })
        pick_obj.do_partial(cr, uid, picking_ids, partial_datas, context=context)
        return {'type': 'ir.actions.act_window_close'}
stock_partial_picking()


class stock_partial_move(osv.osv_memory):
    _inherit = "stock.partial.move"
    
    
    def __create_partial_move_memory(self, move):
        move_memory = super(stock_partial_move,self).__create_partial_move_memory(move)
        move_memory.update({'invoice_qty': move.invoice_qty})
        return move_memory
    
    def do_partial(self, cr, uid, ids, context=None):
        """ Makes partial moves and pickings done.
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param fields: List of fields for which we want default values
        @param context: A standard dictionary
        @return: A dictionary which of fields with values.
        """
    
        if context is None:
            context = {}
        move_obj = self.pool.get('stock.move')
        
        move_ids = context.get('active_ids', False)
        partial = self.browse(cr, uid, ids[0], context=context)
        partial_datas = {
            'delivery_date' : partial.date
        }
        
        p_moves = {}
        picking_type = self.__get_picking_type(cr, uid, move_ids)
        
        moves_list = picking_type == 'product_moves_in' and partial.product_moves_in  or partial.product_moves_out
        for product_move in moves_list:
            p_moves[product_move.move_id.id] = product_move
            
        moves_ids_final = []
        for move in move_obj.browse(cr, uid, move_ids, context=context):
            if move.state in ('done', 'cancel'):
                continue
            if not p_moves.get(move.id):
                continue
            partial_datas['move%s' % (move.id)] = {
                'product_id' : p_moves[move.id].product_id.id,
                'product_qty' : p_moves[move.id].quantity,
                'invoice_qty': p_moves[move.id].invoice_qty,
                'product_uom' :p_moves[move.id].product_uom.id,
                'prodlot_id' : p_moves[move.id].prodlot_id.id,
            }
            
            moves_ids_final.append(move.id)
            if (move.picking_id.type == 'in') and (move.product_id.cost_method == 'average'):
                partial_datas['move%s' % (move.id)].update({
                    'product_price' : p_moves[move.id].cost,
                    'product_currency': p_moves[move.id].currency.id,
                })
                
            
        move_obj.do_partial(cr, uid, moves_ids_final, partial_datas, context=context)
        return {'type': 'ir.actions.act_window_close'}


stock_partial_move()

class split_in_production_lot(osv.osv_memory):
    _inherit = "stock.move.split"
    _columns = {
                
                'invoice_qty': fields.float('Invoice qty'),
                }
    
    
    def split(self, cr, uid, ids, move_ids, context=None):
        """ To split stock moves into production lot
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: the ID or list of IDs if we want more than one
        @param move_ids: the ID or list of IDs of stock move we want to split
        @param context: A standard dictionary
        @return:
        """
        if context is None:
            context = {}
        inventory_id = context.get('inventory_id', False)
        prodlot_obj = self.pool.get('stock.production.lot')
        inventory_obj = self.pool.get('stock.inventory')
        move_obj = self.pool.get('stock.move')
        new_move = []
        for data in self.browse(cr, uid, ids, context=context):
            for move in move_obj.browse(cr, uid, move_ids, context=context):
                move_qty = move.product_qty
                inv_qty = move.invoice_qty
                quantity_rest = move.product_qty
                inv_rest = move.invoice_qty
                uos_qty_rest = move.product_uos_qty
                new_move = []
                if data.use_exist:
                    lines = [l for l in data.line_exist_ids if l]
                else:
                    lines = [l for l in data.line_ids if l]
                total_move_qty = 0.0
                for line in lines:
                    quantity = line.quantity
                    inv_quantity = line.invoice_qty
                    total_move_qty += quantity
                    if total_move_qty > move_qty:
                        raise osv.except_osv(_('Processing Error'), _('Processing quantity %d for %s is larger than the available quantity %d!')\
                                     %(total_move_qty, move.product_id.name, move_qty))
                    if quantity <= 0 or move_qty == 0:
                        continue
                    quantity_rest -= quantity
                    inv_rest -= inv_quantity
                    uos_qty = quantity / move_qty * move.product_uos_qty
                    uos_qty_rest = quantity_rest / move_qty * move.product_uos_qty
                    if quantity_rest < 0:
                        quantity_rest = quantity
                        break
                    default_val = {
                        'product_qty': quantity,
                        'invoice_qty': inv_quantity,
                        'product_uos_qty': uos_qty,
                        'state': move.state
                    }
                    if quantity_rest > 0:
                        current_move = move_obj.copy(cr, uid, move.id, default_val, context=context)
                        if inventory_id and current_move:
                            inventory_obj.write(cr, uid, inventory_id, {'move_ids': [(4, current_move)]}, context=context)
                        new_move.append(current_move)

                    if quantity_rest == 0:
                        current_move = move.id
                    prodlot_id = False
                    if data.use_exist:
                        prodlot_id = line.prodlot_id.id
                    if not prodlot_id:
                        prodlot_id = prodlot_obj.create(cr, uid, {
                            'name': line.name,
                            'product_id': move.product_id.id},
                        context=context)

                    move_obj.write(cr, uid, [current_move], {'prodlot_id': prodlot_id, 'state':move.state})

                    update_val = {}
                    if quantity_rest > 0:
                        update_val['product_qty'] = quantity_rest
                        update_val['invoice_qty'] = inv_rest
                        update_val['product_uos_qty'] = uos_qty_rest
                        update_val['state'] = move.state
                        move_obj.write(cr, uid, [move.id], update_val)

        return new_move

split_in_production_lot()

class stock_move_split_lines(osv.osv_memory):
    _inherit = "stock.move.split.lines"
    _columns = {
                'invoice_qty': fields.float('Invoice qty'),
                }
stock_move_split_lines()
class stock_move_split_lines_exist(osv.osv_memory):
    _inherit = "stock.move.split.lines.exist"
    _columns = {
                'invoice_qty':fields.float('Invoice qty'),
                }
stock_move_split_lines_exist()