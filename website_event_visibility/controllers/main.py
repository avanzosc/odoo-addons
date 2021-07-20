
from odoo import http
from odoo.http import request
from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventController(WebsiteEventController):

    @http.route()
    def events(self, page=1, **searches):
        res = super(WebsiteEventController, self).events(page, **searches)
        website = request.website
        event_obj = request.env['event.event']

        event_ids = event_obj.sudo().search([('website_published', '=', True)])
        filtered_event_ids = event_ids.filtered(
            lambda e: e.enroll == 'public') if event_ids else None

        values = {}
        domain = []
        if filtered_event_ids and len(filtered_event_ids) < len(event_ids):
            domain += [('id', 'in', filtered_event_ids.ids)]

            step = 12  # Number of events per page
            event_count = len(filtered_event_ids)
            pager = website.pager(
                url="/event",
                url_args=searches,
                total=event_count,
                page=page,
                step=step,
                scope=5)
            order = 'date_begin'
            if searches.get('date', 'all') == 'old':
                order = 'date_begin desc'
            order = 'is_published desc, ' + order
            events = event_obj.search(
                domain, limit=step, offset=pager['offset'], order=order)
            values.update({
                'event_ids': events,
                'pager': pager,
            })
        res.qcontext.update(values)
        return res
