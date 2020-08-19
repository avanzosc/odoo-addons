# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.http_routing.models.ir_http import slug


class WebsiteSupplierZoneFilter(WebsiteSale):

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        ('''/shop/category/<model(''' +
         '''"product.public.category","[('website_id', 'in',''' +
         '''(False, current_website_id))]"):category>'''),
        ('''/shop/category/<model(''' +
         '''"product.public.category","[('website_id', 'in',''' +
         '''(False, current_website_id))]"):category>/page/<int:page>''')
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False,
             zone=None, state=None, city=None, layout='', member=None, **post):
        res = super(WebsiteSupplierZoneFilter, self).shop(
            page, category, search, ppg, **post)
        # Prepare params
        Product = request.env['product.template'].with_context(bin_size=True)
        domain = self._get_search_domain(search, category, res.qcontext[
            'attrib_values'])
        url = "/shop"
        if category:
            url = "/shop/category/%s" % slug(category)
        product_template_ids = list(Product.search(domain)).copy()
        if layout == 'grid':
            res.qcontext['layout_mode'] = 'grid'
            ppg = 6
        else:
            layout = 'list'
            res.qcontext['layout_mode'] = 'list'
            ppg = 8

        zone_ids, state_ids, city_ids = [], [], []
        member_ids = []
        for product in product_template_ids:
            supplier_info_ids = product.seller_ids
            for supplier in supplier_info_ids:
                zone_ids.append(supplier.supplier_zone)
                state_ids.append(supplier.supplier_state)
                city_ids.append(supplier.supplier_city)
                member_ids.append(supplier.name)
        for z in list(zone_ids):
            if z.id is False:
                zone_ids.remove(z)
        for s in list(state_ids):
            if s.id is False:
                state_ids.remove(s)
        for c in list(city_ids):
            if not c:
                city_ids.remove(c)
        for m in list(member_ids):
            if not m:
                member_ids.remove(m)
        zone_ids = list(set(zone_ids))
        state_ids = list(set(state_ids))
        city_ids = list(set(city_ids))
        member_ids = list(set(member_ids))
        zones_total = len(zone_ids)
        states_total = len(state_ids)
        cities_total = len(city_ids)
        member_total = len(member_ids)
        # Check deliver capacity for products
        product_template_ids = self.checkDeliveryCapacity(product_template_ids)
        # Filter data
        product_template_ids = self.filterByZone(zone, product_template_ids)
        product_template_ids = self.filterByState(state, product_template_ids)
        product_template_ids = self.filterByCity(city, product_template_ids)
        product_template_ids = self.filterByMember(member,
                                                   product_template_ids)
        product_count = len(product_template_ids)
        # Forced 4 products per page
        pager = request.website.pager(url=url, total=product_count,
                                      page=page, step=ppg, scope=7,
                                      url_args=post)
        pager_rec = self.recalculatePager(pager, zone, state, city, member,
                                          layout)
        product_ids = []
        for product in product_template_ids:
            product_ids.append(product.id)
        domain += [('id', 'in', product_ids)]
        product_ids = Product.search(domain, limit=ppg, offset=pager_rec[
            'offset'], order=self._get_search_order(post))
        res.qcontext.update({'search_count': product_count,
                             'pager': pager_rec,
                             'products': product_ids})
        res.qcontext.update({'zone_ids': zone_ids,
                             'state_ids': state_ids,
                             'city_ids': city_ids,
                             'member_ids': member_ids,
                             'zones_total': zones_total,
                             'states_total': states_total,
                             'cities_total': cities_total,
                             'members_total': member_total,
                             'zone': zone,
                             'state': state,
                             'city': city
                             })
        return res

    def filterByZone(self, zone, product_template_ids):
        if zone and zone != 'All zones':
            for product in list(product_template_ids):
                search = False
                for supplier in product.seller_ids:
                    if supplier.supplier_zone.id == int(zone):
                        search = True
                        break
                if not search:
                    product_template_ids.remove(product)
        return product_template_ids

    def filterByState(self, state, product_template_ids):
        if state and state != 'All states':
            for product in list(product_template_ids):
                search = False
                for supplier in product.seller_ids:
                    if supplier.supplier_state.id == int(state):
                        search = True
                        break
                if not search:
                    product_template_ids.remove(product)
        return product_template_ids

    def filterByCity(self, city, product_template_ids):
        if city and city != 'All cities':
            for product in list(product_template_ids):
                search = False
                for supplier in product.seller_ids:
                    if supplier.supplier_city == str(city):
                        search = True
                        break
                if not search:
                    product_template_ids.remove(product)
        return product_template_ids

    def filterByMember(self, member, product_template_ids):
        if member and member != 'All members':
            for product in list(product_template_ids):
                search = False
                for supplier in product.seller_ids:
                    if supplier.name.id == int(member):
                        search = True
                        break
                if not search:
                    product_template_ids.remove(product)
        return product_template_ids

    def recalculatePager(self, pager, zone, state, city, member, layout):
        if '?' in pager['page']['url']:
            synbol = '&'
        else:
            synbol = '?'
        page_filter = ''
        if zone:
            page_filter = 'zone=' + str(zone)
        if state:
            page_filter = 'state=' + str(state)
        if city:
            page_filter = 'city=' + str(city)
        if member:
            page_filter = 'member=' + str(member)
        pager['page']['url'] = pager['page'][
            'url'] + synbol + page_filter
        pager['page_start']['url'] = pager['page_start'][
            'url'] + synbol + page_filter
        pager['page_previous']['url'] = pager['page_previous'][
            'url'] + synbol + page_filter
        pager['page_next']['url'] = pager['page_next'][
            'url'] + synbol + page_filter
        pager['page_end']['url'] = pager['page_end'][
            'url'] + synbol + page_filter
        for page in pager['pages']:
            page['url'] = page['url'] + synbol + page_filter
        pager_lay = self.recalculatePagerLayout(pager, layout)
        return pager_lay

    def recalculatePagerLayout(self, pager, layout):
        if '?' in pager['page']['url']:
            synbol = '&'
        else:
            synbol = '?'
        if 'layout=' not in pager['page']['url']:
            pager['page']['url'] = pager['page'][
                'url'] + synbol + "layout=" + layout
            pager['page_start']['url'] = pager['page_start'][
                'url'] + synbol + "layout=" + layout
            pager['page_previous']['url'] = pager['page_previous'][
                'url'] + synbol + "layout=" + layout
            pager['page_next']['url'] = pager['page_next'][
                'url'] + synbol + "layout=" + layout
            pager['page_end']['url'] = pager['page_end'][
                'url'] + synbol + "layout=" + layout
            for page in pager['pages']:
                page['url'] = page['url'] + synbol + "layout=" + layout
        return pager

    # HACER LAS PRUEBAS NECESARIAS
    def checkDeliveryCapacity(self, product_template_ids):
        partner = request.env.user.partner_id
        if not (request.env.user._is_superuser()
                or request.env.user._is_admin()):
            for product in list(product_template_ids):
                search = False
                for supplier in product.seller_ids:
                    if (supplier.name.sends_to == 'all'
                        or (supplier.name.sends_to == 'city' and
                            supplier.supplier_city == partner.city)
                        or (supplier.name.sends_to == 'zone' and
                            supplier.supplier_zone == partner.partner_zone_id)
                        or (supplier.name.sends_to == 'state' and
                            supplier.supplier_state == partner.state_id)):
                        search = True
                        break
                if not search:
                    product_template_ids.remove(product)
        return product_template_ids
