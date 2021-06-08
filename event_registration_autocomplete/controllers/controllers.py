# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.http import request
from odoo.addons.website_event.controllers.main import WebsiteEventController
import werkzeug


class WebsiteEventController(WebsiteEventController):

    @http.route()
    def registration_new(self, event, **post):
        if not event.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        tickets = self._process_tickets_form(event, post)
        availability_check = True
        if event.seats_limited:
            ordered_seats = 0
            for ticket in tickets:
                ordered_seats += ticket['quantity']
            if event.seats_available < ordered_seats:
                availability_check = False
        if not tickets:
            return False
        partner_ids = request.env.user.partner_id.child_ids
        return request.env['ir.ui.view']._render_template(
            "website_event.registration_attendee_details",
            {'tickets': tickets, 'event': event, 'partner_ids': partner_ids,
             'availability_check': availability_check})
