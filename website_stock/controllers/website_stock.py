
from odoo import http, _
from odoo.http import request
from odoo.addons.account.controllers.portal import CustomerPortal

class PortalStock(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalStock, self)._prepare_portal_layout_values()
        partner_id = request.env.user.partner_id
        stock_count = request.env['stock.picking'].search_count([('partner_id','=',partner_id.id)])
        values['stock_count'] = stock_count
        return values    
    
    @http.route(['/my/stock', '/my/stock/<int:stock_picking_id>'], type='http', auth="user", website=True)
    def portal_my_stock(self, stock_picking_id=None):
        values = self._prepare_portal_layout_values()
        partner_id = request.env.user.partner_id
        stock_picking_ids = request.env['stock.picking'].search([('partner_id','=',partner_id.id)])
        
        values.update({
            'stock_picking_ids': stock_picking_ids,
            'page_name': 'stock',
        })
        if stock_picking_id == None:
            return request.render("website_stock.portal_my_stock", values)
        else:
            stock_move_line_ids = request.env['stock.move.line'].search([('picking_id','=',stock_picking_id)])
            stock_picking_id = request.env['stock.picking'].search([('id','=',stock_picking_id)])
            values.update({
                'stock_picking_id': stock_picking_id,
                'stock_move_line_ids': stock_move_line_ids})
            return request.render("website_stock.portal_my_stock_details", values)
    
    