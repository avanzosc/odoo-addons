# -*- coding: utf-8 -*-
# from odoo import http


# class SaleOrderEventAttendee(http.Controller):
#     @http.route('/sale_order_event_attendee/sale_order_event_attendee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_event_attendee/sale_order_event_attendee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_event_attendee.listing', {
#             'root': '/sale_order_event_attendee/sale_order_event_attendee',
#             'objects': http.request.env['sale_order_event_attendee.sale_order_event_attendee'].search([]),
#         })

#     @http.route('/sale_order_event_attendee/sale_order_event_attendee/objects/<model("sale_order_event_attendee.sale_order_event_attendee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_event_attendee.object', {
#             'object': obj
#         })
