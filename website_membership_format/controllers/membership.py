# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request
from odoo.addons.website_membership.controllers.main import WebsiteMembership


class WebsiteMembership(WebsiteMembership):

    @http.route(['/members/<partner_id>'], type='http', auth="public",
                website=True)
    def partners_detail(self, partner_id, **post):
        res = super(WebsiteMembership, self).partners_detail(partner_id,
                                                             **post)
        products = request.env['product.supplierinfo'].search(
            [('name', '=', res.qcontext['partner'].id)])
        res.qcontext.update({'products': products})
        return res

    @http.route([
        '/members',
        '/members/page/<int:page>',
        '/members/association/<membership_id>',
        '/members/association/<membership_id>/page/<int:page>',

        '/members/country/<int:country_id>',
        '/members/country/<country_name>-<int:country_id>',
        '/members/country/<int:country_id>/page/<int:page>',
        '/members/country/<country_name>-<int:country_id>/page/<int:page>',

        ('/members/association/<membership_id>/country/<country_name>-' +
         '<int:country_id>'),
        '/members/association/<membership_id>/country/<int:country_id>',
        ('/members/association/<membership_id>/country/<country_name>-' +
         '<int:country_id>/page/<int:page>'),
        ('/members/association/<membership_id>/country/<int:country_id>' +
         '/page/<int:page>'),
    ], type='http', auth="public", website=True)
    def members(self, membership_id=None, country_name=None, country_id=0,
                page=1, zone=None, state=None, city=None, **post):
        res = super(WebsiteMembership, self).members(
            membership_id, country_name, country_id, page, **post)

        zone_ids, state_ids, city_ids, member_ids = [], [], [], {}
        for partner in res.qcontext['partners'].values():
            zone_ids.append(partner.partner_zone_id)
            state_ids.append(partner.state_id)
            city_ids.append(partner.city)
            member_ids[partner.id] = partner
        zone_ids = list(set(zone_ids))
        state_ids = list(set(state_ids))
        city_ids = list(set(city_ids))
        for z in list(zone_ids):
            if z.id is False:
                zone_ids.remove(z)
        for s in list(state_ids):
            if s.id is False:
                state_ids.remove(s)
        for c in list(city_ids):
            if not c:
                city_ids.remove(c)
        zones_total = len(zone_ids)
        states_total = len(state_ids)
        cities_total = len(city_ids)
        # Filter data
        member_ids = self.filterByZone(zone, member_ids)
        member_ids = self.filterByState(state, member_ids)
        member_ids = self.filterByCity(city, member_ids)
        pager = self.recalculatePager(res.qcontext['pager'], zone, state, city)
        res.qcontext['memberships_partner_ids']['free'] = list(
            member_ids.keys())
        res.qcontext.update({
            'states_total': states_total,
            'zones_total': zones_total,
            'cities_total': cities_total,
            'state_ids': state_ids,
            'zone_ids': zone_ids,
            'city_ids': city_ids,
            'partners': member_ids,
            'pager': pager
            })
        return res

    def filterByZone(self, zone, member_ids):
        if zone and zone != 'All zones':
            for key, value in list(member_ids.items()):
                if value.partner_zone_id.id != int(zone):
                    member_ids.pop(key)
        return member_ids

    def filterByState(self, state, member_ids):
        if state and state != 'All states':
            for key, value in list(member_ids.items()):
                if value.state_id.id != int(state):
                    member_ids.pop(key)
        return member_ids

    def filterByCity(self, city, member_ids):
        if city and city != 'All cities':
            for key, value in list(member_ids.items()):
                if value.city != str(city):
                    member_ids.pop(key)
        return member_ids

    def recalculatePager(self, pager, zone, state, city):
        if '?' not in pager['page']['url']:
            page_filter = '?'
        else:
            page_filter = ''
        if zone:
            page_filter += '&zone=' + str(zone)
        if state:
            page_filter += '&state=' + str(state)
        if city:
            page_filter += '&city=' + str(city)
        if '?&' in page_filter:
            page_filter = page_filter.replace('&', '', 1)
        pager['page']['url'] = pager['page'][
            'url'] + page_filter
        pager['page_first']['url'] = pager['page_first'][
            'url'] + page_filter
        pager['page_start']['url'] = pager['page_start'][
            'url'] + page_filter
        pager['page_previous']['url'] = pager['page_previous'][
            'url'] + page_filter
        pager['page_next']['url'] = pager['page_next'][
            'url'] + page_filter
        pager['page_end']['url'] = pager['page_end'][
            'url'] + page_filter
        pager['page_last']['url'] = pager['page_last'][
            'url'] + page_filter
        for page in pager['pages']:
            page['url'] = page['url'] + page_filter
        return pager
