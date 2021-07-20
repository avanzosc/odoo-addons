

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        event_obj = request.env['event.event']
        course_obj = request.env['slide.channel']

        values['event_count'] = event_obj.search_count([
            ('is_participating', '=', True)
        ]) if event_obj.check_access_rights(
            'read', raise_exception=False) else 0

        values['learning_count'] = course_obj.search_count([
            ('is_member', '=', True)
        ]) if event_obj.check_access_rights(
            'read', raise_exception=False) else 0

        return values

    @http.route(['/my/events', '/my/events/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_events(self, page=1, date_begin=None, date_end=None,
                         sortby=None, search_in='all', **kw):

        event_obj = request.env['event.event']
        website = request.website

        domain = [('is_participating', '=', True)]
        order = 'date_begin desc'
        events = event_obj.sudo().search(domain, order=order)

        step = 12  # Number of events per page
        course_count = len(events)
        pager = website.pager(
            url="/my/events",
            url_args=None,
            total=course_count,
            page=page,
            step=step,
            scope=5)

        events = event_obj.search(
            domain, limit=step, offset=pager['offset'], order=order)

        values = {
            'events': events,
            'pager': pager
        }

        return request.render(
            "website_portal_event_learning.portal_my_events", values)

    @http.route(['/my/courses', '/my/courses/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_courses(self, page=1, date_begin=None, date_end=None,
                          sortby=None, search_in='all', **kw):

        course_obj = request.env['slide.channel']
        website = request.website

        domain = [('is_member', '=', True)]
        courses = course_obj.sudo().search(domain)

        step = 12  # Number of events per page
        course_count = len(courses)
        pager = website.pager(
            url="/my/courses",
            url_args=None,
            total=course_count,
            page=page,
            step=step,
            scope=5)

        courses = course_obj.search(domain, limit=step, offset=pager['offset'])

        values = {
            'courses': courses,
            'pager': pager
        }

        return request.render(
            "website_portal_event_learning.portal_my_courses", values)
