##############################################################################
#
# Copyright (c) 2010 NaN Projectes de Programari Lliure, S.L.  All Rights Reserved.
#                    http://www.NaN-tic.com
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import time
from osv import osv, fields
from tools import config
from tools.translate import _

class sale_order(osv.osv):
    _inherit = 'sale.order'

    def _amount_all(self, cr, uid, ids, field_name, arg, context):
        result = super(sale_order, self)._amount_all(cr, uid, ids, field_name, arg, context)
        for order in self.browse(cr, uid, ids, context):
            if order.prices_used != 'openerp_prices':
                amount_tax = 0.0
                amount_untaxed = 0.0
                amount_total = 0.0
                if order.prices_used == 'external_line_prices':
                    for line in order.order_line:
                        if line.prices_used == 'external_line_prices':
                            amount_tax += line.external_tax_amount
                            amount_untaxed += line.external_base_amount
                        else:
                            for line_tax in line.tax_id:
                                amount_tax += line_tax.amount * line.price_subtotal
                            amount_untaxed += line.price_subtotal
                    amount_total = amount_untaxed + amount_tax
                elif order.prices_used == 'external_total_prices':
                    amount_tax = order.external_sale_tax_amount
                    amount_untaxed = order.external_sale_base_amount
                    amount_total = order.external_sale_total_amount
                result[ order.id ] = {
                    'amount_tax': amount_tax,
                    'amount_untaxed': amount_untaxed,
                    'amount_total': amount_total,
                }
        return result

    def _get_order(self, cr, uid, ids, context={}):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    _columns = {
        # Inherited fields
        'amount_untaxed': fields.function(_amount_all, method=True, digits=(16, 4), string='Untaxed Amount',
            store = {
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','prices_used', 'external_sale_base_amount', 'external_sale_tax_amount', 'external_sale_total_amount'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty', 'prices_used', 'external_tax_amount', 'external_base_amount', 'external_tax_percent'], 10),
            }, multi='sums'),
        'amount_tax': fields.function(_amount_all, method=True, digits=(16,4), string='Taxes',
            store = {
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','prices_used', 'external_sale_base_amount', 'external_sale_tax_amount', 'external_sale_total_amount'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty', 'prices_used', 'external_tax_amount', 'external_base_amount', 'external_tax_percent'], 10),
            }, multi='sums'),
        'amount_total': fields.function(_amount_all, method=True, digits=(16,4), string='Total',
            store = {
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','prices_used', 'external_sale_base_amount', 'external_sale_tax_amount', 'external_sale_total_amount'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty', 'prices_used', 'external_tax_amount', 'external_base_amount', 'external_tax_percent'], 10),
            }, multi='sums'),
        # Added fields
        'prices_used': fields.selection( [
            ( 'openerp_prices', 'Use OpenERP Prices' ),
            ( 'external_line_prices' , 'Use External Lines Prices' ),
            ( 'external_total_prices', 'Use External Total Prices' ),
        ], 'Prices Used', help="Select which prices OpenERP have to use to calculate the Invoice. 'Use OpenERP Price', use the OpenERP calcualted prices; 'Use External Lines Prices', use prices imported from the lines of the external system or online shop; 'Use External Total Prices', use the total prices imported from external system or online shop." ),
        'external_sale_base_amount': fields.float( 'External Subtotal', digits=(16,4), readonly=True, help='Total amount in external system or online shop if the order was imported.' ),

        'external_sale_tax_amount': fields.float( 'External Tax', digits=(16,4), readonly=True, help='Tax Amount in external system or online shop if the order was imported.' ),
        'external_sale_total_amount': fields.float( 'External Total', digits=(16,4), readonly=True, help='Total amount in external system or online shop if the order was imported.' ),
    }

    _defaults = {
        'prices_used': lambda *a: 'openerp_prices',
    }

    def _inv_get(self, cr, uid, order, context={}):
        result = super(sale_order, self)._inv_get(cr, uid, order, context)
        result['prices_used'] = order.prices_used
        result[ 'external_sale_base_amount' ] = order.external_sale_base_amount
        result[ 'external_sale_tax_amount' ] = order.external_sale_tax_amount
        result[ 'external_sale_total_amount' ] = order.external_sale_total_amount
        return result

    def write( self, cr, uid, ids, vals, context=None ):
        for order in self.browse( cr, uid, ids, context ):
            if ( vals.get( 'prices_used' ) and vals[ 'prices_used' ] == 'openerp_prices' ) or ( not vals.get( 'prices_used' ) and order.prices_used == 'openerp_prices' ):
                continue
            if vals.get( 'order_line' ):
                for orderline in vals[ 'order_line' ]:
                    if orderline[ 1 ] == 0 and order.prices_used == 'external_total_prices':
                        raise osv.except_osv( _( 'Error' ), _( "Sale order %s can not have a non-imported line (%s) because total amounts are not calculated, they are imported from an external application/shop." ) %  ( order.name, orderline[ 2 ][ 'name' ] ) )
                    order_line_stored = self.pool.get( 'sale.order.line' ).browse( cr, uid, orderline[ 1 ], context=context )
                    field_mod = []
                    if order_line_stored.product_uos_qty != orderline[ 2 ][ 'product_uos_qty' ]:
                        field_mod.append( _( "Quantity (UoS)" ) )
                    if order_line_stored.product_uom_qty != orderline[ 2 ][ 'product_uom_qty' ]:
                        field_mod.append( _( "Quantity (UoM)" ) )
                    if order_line_stored.price_unit != orderline[ 2 ][ 'price_unit' ]:
                        field_mod.append( _( "Unit Price" ) )
                    if order_line_stored.discount != orderline[ 2 ][ 'discount' ]:
                        field_mod.append( _( "Discount (%)" ) )
                    if order_line_stored.tax_id and len( order_line_stored.tax_id ) != 1 or order_line_stored.tax_id[ 0 ].id != orderline[ 2 ][ 'tax_id' ][ 0 ][ 2 ][ 0 ]:
                        field_mod.append( _( "Taxes" ) )

                    if field_mod:
                        field_mod = ",".join( field_mod )
                        raise osv.except_osv( _( 'Error' ), _( "Field(s) %s of line %s in sale order %s can not be edited because total amounts are not calculated, they are imported from an external application/shop." ) % ( field_mod, order_line_stored.name, order.name ) )

        result = super( sale_order, self ).write( cr, uid, ids, vals, context )

        for order in self.browse( cr, uid, ids, context ):
            for orderline in order.order_line: 
                #if order.prices_used == 'external_total_prices' and orderline.prices_used != 'external_total_prices':
                if ( vals.get( 'prices_used' ) and vals[ 'prices_used' ] == 'external_total_prices' or order.prices_used == 'external_total_prices' ) and orderline.prices_used != 'external_total_prices':
                    raise osv.except_osv( _( 'Error' ), _( "Sale order %s can not have a non-imported line because total amounts are not calulated, they are imported from an external application/shop." ) % order.name )

        return result

sale_order()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    def _amount_line(self, cr, uid, ids, field_name, arg, context):
        result = super(sale_order_line, self)._amount_line(cr, uid, ids, field_name, arg, context)
        for line in self.browse(cr, uid, ids, context):
            if line.order_id.prices_used == 'external_line_prices' and line.prices_used == 'external_line_prices':
                result[line.id] = line.external_base_amount
        return result

    _columns = {
        # Inherited field
        'price_subtotal': fields.function(_amount_line, method=True, string='Subtotal', digits=(16, 4)),
        # Added fields
        'prices_used': fields.selection( [
            ( 'openerp_prices', 'Use OpenERP Prices' ),
            ( 'external_line_prices' , 'Use External Lines Prices' ),
            ( 'external_total_prices', 'Use External Total Prices' ),
        ], 'Prices Used', readonly=True, help="Select which prices OpenERP have to use to calculate the Invoice. 'Use OpenERP Price', use the OpenERP calcualted prices; 'Use External Lines Prices', use prices imported from the lines of the external system or online shop; 'Use External Total Prices', use the total prices imported from external system or online shop." ),
        'external_tax_amount': fields.float('External Tax', digits=(16,4), readonly=True, help='Tax Amount in external system or online shop if the order was imported.'),
        'external_base_amount': fields.float('External Base Raw Total', digits=(16,4), readonly=True, help='Base amount in external system or online shop if the order was imported.'),

        'external_tax_percent': fields.float('External Tax Percent', digits=(16,4), readonly=True, help='Tax Percentage Applied in online shop.'),
        'external_base_original_price': fields.float('External Original Base Price', digits=(16, 4), readonly=True, help='Original Base Price in online shop.'),
        'external_base_tax_amount': fields.float('External Base Tax Amount', digits=(16, 4), readonly=True, help='Base Tax Amount in online shop.'),
    }

    _defaults = {
        'prices_used': lambda *a: 'openerp_prices',
    }

    def invoice_line_create(self, cr, uid, ids, context={}):
        result = super(sale_order_line, self).invoice_line_create(cr, uid, ids, context)
        for line in self.browse(cr, uid, ids, context):
            # Note: We only support the case when the *order line* is invoiced *all at once*.
            # Cases in which the same order line has several invoice lines will not work properly.
            for invoice_line in line.invoice_lines:
                self.pool.get('account.invoice.line').write(cr, uid, invoice_line.id, {
                    'prices_used': line.prices_used,
                    'external_tax_amount': line.external_tax_amount,
                    'external_base_amount': line.external_base_amount,
                }, context)
        return result

sale_order_line()

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def _amount_all( self, cr, uid, ids, name, args, context=None ):
        result = super( account_invoice, self )._amount_all( cr, uid, ids, name, args, context )
        for invoice in self.browse( cr, uid, ids, context=context ):
            if invoice.prices_used != 'openerp_prices':
                amount_tax = 0.0
                amount_untaxed = 0.0
                amount_total = 0.0
                if invoice.prices_used == 'external_line_prices':
                    for line in invoice.invoice_line:
                        if line.prices_used == 'external_line_prices':
                            amount_untaxed += line.external_base_amount
                        else:
                            amount_untaxed += line.price_subtotal
                    for line in invoice.tax_line:
                        if line.prices_used == 'external_line_prices':
                            amount_tax += line.external_tax_amount
                        else:
                            for line_tax in line.invoice_line_tax_id:
                                amount_tax += line_tax.amount * line.price_subtotal
                    amount_total = amount_tax + amount_untaxed
                elif invoice.prices_used == 'external_total_prices':
                    amount_tax = invoice.external_sale_tax_amount
                    amount_untaxed = invoice.external_sale_base_amount
                    amount_total = invoice.external_sale_total_amount
                result[ invoice.id ] = {
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_total,
                }
        return result

    def _get_invoice_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.invoice.line').browse(cr, uid, ids, context=context):
            result[line.invoice_id.id] = True
        return result.keys()

    def _get_invoice_tax(self, cr, uid, ids, context=None):
        result = {}
        for tax in self.pool.get('account.invoice.tax').browse(cr, uid, ids, context=context):
            result[tax.invoice_id.id] = True
        return result.keys()

    _columns = {
        # Inherited field
        'amount_untaxed': fields.function(_amount_all, method=True, digits=(16, 4),string='Untaxed',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line', 'prices_used', 'external_sale_base_amount', 'external_sale_tax_amount', 'external_sale_total_amount'], 20),
                'account.invoice.tax': (_get_invoice_tax, None, 20),
                'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount', 'prices_used', 'external_base_amount', 'external_tax_amount'], 20),
            },
            multi='all'),
        'amount_tax': fields.function(_amount_all, method=True, digits=(16, 4), string='Tax',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line', 'prices_used', 'external_sale_base_amount', 'external_sale_tax_amount', 'external_sale_total_amount'], 20),
                'account.invoice.tax': (_get_invoice_tax, None, 20),
                'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount', 'prices_used', 'external_base_amount', 'external_tax_amount'], 20),
            },
            multi='all'),
        'amount_total': fields.function(_amount_all, method=True, digits=(16, 4), string='Total',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line', 'prices_used', 'external_sale_base_amount', 'external_sale_tax_amount', 'external_sale_total_amount'], 20),
                'account.invoice.tax': (_get_invoice_tax, None, 20),
                'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount', 'prices_used', 'external_base_amount', 'external_tax_amount'], 20),
            },
            multi='all'),
        # Added fields
        'prices_used': fields.selection( [
            ( 'openerp_prices', 'Use OpenERP Prices' ),
            ( 'external_line_prices' , 'Use External Lines Prices' ),
            ( 'external_total_prices', 'Use External Total Prices' ),
        ], 'Prices Used', help="Select which prices OpenERP have to use to calculate the Invoice. 'Use OpenERP Price', use the OpenERP calcualted prices; 'Use External Lines Prices', use prices imported from the lines of the external system or online shop; 'Use External Total Prices', use the total prices imported from external system or online shop." ),
        'external_sale_base_amount': fields.float( 'External Subtotal Invoiced', digits=(16,4), readonly=True, help='Total amount in external system or online shop if the order was imported.' ),
        'external_sale_tax_amount': fields.float( 'External Tax Invoiced', digits=(16,4), readonly=True, help='Tax Amount in external system or online shop if the order was imported.' ),
        'external_sale_total_amount': fields.float( 'External Total Invoiced', digits=(16,4), readonly=True, help='Total amount in external system or online shop if the order was imported.' ),
    }

    _defaults = {
        'prices_used': lambda *a: 'openerp_prices',
    }

    def write( self, cr, uid, ids, vals, context=None ):
        for invoice in self.browse( cr, uid, ids, context ):
            if ( vals.get( 'prices_used' ) and vals[ 'prices_used' ] == 'openerp_prices' ) or ( not vals.get( 'prices_used' ) and invoice.prices_used == 'openerp_prices' ):
                continue
            if vals.get( 'invoice_line' ):
                for invoiceline in vals[ 'invoice_line' ]:
                    if invoiceline[ 1 ] == 0 and invoice.prices_used == 'external_total_prices':
                        raise osv.except_osv( _( 'Error' ), _( "Invoice %s can not have a non-imported line (%s) because total amounts are not calculated, they are imported from an external application/shop." ) % ( invoice.number, invoiceline[ 2 ][ 'name' ] ) )
                    invoice_line_stored = self.pool.get( 'account.invoice.line' ).browse( cr, uid, invoiceline[ 1 ], context=context )
                    field_mod = []
                    if invoice_line_stored.price_unit != invoiceline[ 2 ][ 'price_unit' ]:
                        field_mod.append( _( "Unit Price" ) )
                    if invoice_line_stored.quantity != invoiceline[ 2 ][ 'quantity' ]:
                        field_mod.append( _( "Quantity" ) )
                    if invoice_line_stored.discount != invoiceline[ 2 ][ 'discount' ]:
                        field_mod.append( _( "Discount (%)" ) )
                    if invoice_line_stored.invoice_line_tax_id and len( invoice_line_stored.invoice_line_tax_id ) != 1 or invoice_line_stored.invoice_line_tax_id[ 0 ].id != invoiceline[ 2 ][ 'invoice_line_tax_id' ][ 0 ][ 2 ][ 0 ]:
                        field_mod.append( _( "Taxes" ) )

                    if field_mod:
                        field_mod = ",".join( field_mod )
                        raise osv.except_osv( _( 'Error' ), _( "Field(s) %s of line %s in invoice %s can not be edited because total amounts are not calculated, they are imported from an external application/shop." ) % ( field_mod, invoice_line_stored.name, invoice.name ) )
        result = super( account_invoice, self ).write( cr, uid, ids, vals, context )

        for invoice in self.browse( cr, uid, ids, context ):
            for invoiceline in invoice.invoice_line: 
                if invoice.prices_used == 'external_total_prices' and invoiceline.prices_used != 'external_total_prices':
                    raise osv.except_osv( _( 'Error' ), _( "Invoice %s can not have a non-imported line because total amounts are not calulated, they are imported from an external application/shop." ) % invoice.name )
        return result

account_invoice()

class account_invoice_tax(osv.osv):
    _inherit = 'account.invoice.tax'

    def compute(self, cr, uid, invoice_id, context={}):
        tax_grouped = super(account_invoice_tax, self).compute(cr, uid, invoice_id, context)
        invoice = self.pool.get('account.invoice').browse(cr, uid, invoice_id, context)
        if invoice.prices_used != 'openerp_prices':
            company_currency = invoice.company_id.currency_id.id
            if len(tax_grouped) > 1:
                raise osv.except_osv(_('Error'), _('There should be only one tax line when external prices are used.'))
            for taxes in tax_grouped.values():
                tax = 0.0
                base = 0.0
                for line in invoice.invoice_line:
                    if line.prices_used == 'external_line_prices':
                        base += line.external_base_amount
                        tax += line.external_tax_amount
                    else:
                        base += line.price_subtotal
                        for line_tax in line.invoice_line_tax_id:
                            tax += line_tax.amount * line.price_subtotal
                if invoice.prices_used == 'external_total_prices':
                    base = invoice.external_sale_base_amount
                    taxes['amount'] = invoice.external_sale_tax_amount
                elif invoice.prices_used == 'external_line_prices':
                    taxes['amount'] = tax
                else:
                    taxes['amount'] = 0.0
                taxes['base'] = base
                taxes['base_amount'] = self.pool.get('res.currency').compute(cr, uid, invoice.currency_id.id, company_currency, taxes['base'], context={'date': invoice.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
                taxes['tax_amount'] = self.pool.get('res.currency').compute(cr, uid, invoice.currency_id.id, company_currency, taxes['amount'], context={'date': invoice.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
        return tax_grouped

account_invoice_tax()

class account_invoice_line(osv.osv):
    _inherit = 'account.invoice.line'

    def _amount_line(self, cr, uid, ids, field_name, arg, context):
        result = super(account_invoice_line, self)._amount_line(cr, uid, ids, field_name, arg, context)
        for line in self.browse(cr, uid, ids, context):
            if line.invoice_id.prices_used == 'external_line_prices' and line.prices_used == 'external_line_prices':
                result[line.id] = line.external_base_amount
        return result

    def _amount_line2(self, cr, uid, ids, field_name, arg, context):
        result = super(account_invoice_line, self)._amount_line2(cr, uid, ids, field_name, arg, context)
        for line in self.browse(cr, uid, ids, context):
            if line.invoice_id.prices_used == 'external_line_prices' and line.prices_used == 'external_line_prices':
                result[line.id]['price_subtotal_incl'] = line.external_base_amount + line.external_tax_amount
        return result

    def _get_invoice(self, cr, uid, ids, context):
        result = {}
        for inv in self.pool.get('account.invoice').browse(cr, uid, ids, context=context):
            for line in inv.invoice_line:
                result[line.id] = True
        return result.keys()

    _columns = {
        # Inherited field
        'price_subtotal': fields.function(_amount_line, method=True, string='Subtotal',store=True, type="float", digits=(16, 4)),

        # Inherited field from module account_tax_include
        'price_subtotal_incl': fields.function(_amount_line2, method=True, string='Subtotal', multi='amount', store={
            'account.invoice': (_get_invoice,['price_type', 'prices_used'],10), 
            'account.invoice.line': (lambda self,cr,uid,ids,c={}: ids,None,10)
        }),

        # Added fields
        'prices_used': fields.selection( [
            ( 'openerp_prices', 'Use OpenERP Prices' ),
            ( 'external_line_prices' , 'Use External Lines Prices' ),
            ( 'external_total_prices', 'Use External Total Prices' ),
        ], 'Prices Used', readonly=True, help="Select which prices OpenERP have to use to calculate the Invoice. 'Use OpenERP Price', use the OpenERP calcualted prices; 'Use External Lines Prices', use prices imported from the lines of the external system or online shop; 'Use External Total Prices', use the total prices imported from external system or online shop." ),
        'external_tax_amount': fields.float('External Tax Invoiced', digits=(16, 4), readonly=True, help='Tax Amount in external system or online shop if the invoice or the corresponding order was imported.'),
        'external_base_amount': fields.float('External Base Raw Total', digits=(16, 4), readonly=True, help='Base amount in external system or online shop if the invoice or the corresponding order was imported.'),
    }

    _defaults = {
        'prices_used': lambda *a: 'openerp_prices',
    }

account_invoice_line()

class stock_picking( osv.osv ):
    _inherit = "stock.picking"

    def action_invoice_create( self, cursor, user, ids, journal_id=False, group=False, type='out_invoice', context=None ):
        if self.browse(cursor,user,ids[0]).type == 'out':
            result = super( stock_picking, self ).action_invoice_create( cursor, user, ids, journal_id, group, type, context )
            invoice_line_obj = self.pool.get( 'account.invoice.line' )
            sale_line_obj = self.pool.get( 'sale.order.line' )
            for pick_id, invoice_id in result.iteritems():
                pick_order = self.browse( cursor, user, pick_id, context )
                sale = self.pool.get( 'sale.order' ).browse( cursor, user, pick_order.sale_id.id, context )
                for invoice_line_id in invoice_line_obj.search( cursor, user, [ ( 'invoice_id', '=', invoice_id ) ] ):
                    invoiceline = invoice_line_obj.browse( cursor, user, invoice_line_id, context )
                    orderline_id = sale_line_obj.search( cursor, user, [ ( 'order_id', '=', sale.id ), ( 'product_id', '=', invoiceline.product_id.id ) ] )[ 0 ]
                    orderline = sale_line_obj.browse( cursor, user, orderline_id, context )
                    invoice_line_obj.write( cursor, user, [ invoice_line_id ], {
                                                                            'prices_used': orderline.prices_used,
                                                                            'external_tax_amount': orderline.external_tax_amount,
                                                                            'external_base_amount': orderline.external_base_amount,
                                                                            }, context )
                    self.pool.get( 'account.invoice' ).write( cursor, user, [ invoice_id ], {
                                                                                    'prices_used': pick_order.sale_id.prices_used,
                                                                                    'external_sale_base_amount' : pick_order.sale_id.external_sale_base_amount,
                                                                                    'external_sale_tax_amount' : pick_order.sale_id.external_sale_tax_amount,
                                                                                    'external_sale_total_amount' : pick_order.sale_id.external_sale_total_amount,
                                                                                    }, context )
        else:
            result = super( stock_picking, self ).action_invoice_create( cursor, user, ids, journal_id, group, type, context )
    	return result

stock_picking()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
