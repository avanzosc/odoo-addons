
from odoo import http
from odoo.http import request
from datetime import datetime
from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventController(WebsiteEventController):

    @http.route()
    def events(self, page=1, **searches):
        res = super(WebsiteEventController, self).events(page, **searches)
        values = {}
        logged_user = request.env['res.users'].browse(request.uid)
        logged_partner = logged_user.partner_id
        domain = request.website.website_domain()
        today = datetime.today()
        domain += [
            ('date_begin', '>=', today),
            '|',
            ('education_center_ids', '=', False),
            ('education_center_ids', '=', logged_partner.current_center_id.id),
            '|',
            ('education_group_ids', '=', False),
            ('education_group_ids', '=', logged_partner.current_group_id.id),
            '|',
            ('education_course_ids', '=', False),
            ('education_course_ids', '=', logged_partner.current_course_id.id),
        ]

        event_obj = request.env[
            'event.event']
        total = event_obj.search_count(domain)

        step = 10  # Number of events per page
        pager = request.website.pager(
            url='/event',
            total=total,
            page=page,
            step=step,
        )
        events = event_obj.search(
            domain, offset=(page - 1) * step,
            limit=step)

        dates = res.qcontext.get('dates')
        for index, date in enumerate(dates):
            event_recount = events.search_count(domain+date[2])
            date[3] = event_recount
            dates[index] = date

        values.update({
            'pager': pager,
            'event_ids': events,
            'dates': dates
        })
        res.qcontext.update(values)
        return res
