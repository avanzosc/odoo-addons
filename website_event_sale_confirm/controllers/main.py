
import werkzeug
from odoo import http
from odoo.http import request
from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController


class WebsiteEventSaleController(WebsiteEventSaleController):

    # THIS FUNCTION REPLACES THE SUPER
    @http.route()
    def registration_confirm(self, event, **post):
        if not event.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        registrations = self._process_attendees_form(event, post)
        attendees_sudo = self._create_attendees_from_registration_post(event,
                                                                       registrations)
        # we have at least one registration linked to a ticket -> sale mode activate
        if any(info['event_ticket_id'] for info in registrations):
            order = request.website.sale_get_order(force_create=False)
            if order.amount_total:
                return request.redirect("/shop/checkout")
            # free tickets -> order with amount = 0: auto-confirm, no checkout
            elif order and self.confirm_free_ticket(order):
                order.action_confirm()  # tde notsure: email sending ?
                request.website.sale_reset()

        return request.render("website_event.registration_complete",
                              self._get_registration_confirm_values(event,
                                                                    attendees_sudo))

    def confirm_free_ticket(self, order):
        confirm = False
        for line in order.order_line:
            if line.event_ticket_id and line.event_ticket_id.confirm_free_ticket:
                confirm = True
        return confirm
