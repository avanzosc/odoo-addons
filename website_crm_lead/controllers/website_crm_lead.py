
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalCrmLead(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalCrmLead, self)._prepare_portal_layout_values()
        partner_and_leads = self.get_partners_by_connected_user(
            'crm.lead')
        values.update({
            'crm_lead_partner_ids': list(set(partner_and_leads['partners'])),
            'crm_lead_count': len(partner_and_leads['model_objs']),
            'crm_lead_ids': partner_and_leads['model_objs'],
            'page_name': 'crm_lead',
        })
        return values

    @http.route(['/my/crm_lead', '/my/crm_lead/<int:crm_lead_id>',
                 '/my/crm_lead/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_crm_lead(self, crm_lead_id=None, page=1, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Crm_lead = request.env['crm.lead']
        # searchbar_sortings = self.get_query_order(sortby)
        filtered_lead = self.filter_data([], 'crm.lead', **kw)
        filtered_lead_ids = []
        for lead in filtered_lead:
            if lead in values['crm_lead_ids']:
                filtered_lead_ids.append(lead.id)
        domain = [('id', 'in', filtered_lead_ids)]
        lead_count = Crm_lead.sudo().search_count(domain)
        pager = portal_pager(
            url="/my/crm_lead",
            total=lead_count,
            page=page,
            step=self._items_per_page
        )
        pager = self.recalculatePager(pager, **kw)
        leads = Crm_lead.sudo().search(
            domain, limit=self._items_per_page,
            offset=pager['offset'])
        if crm_lead_id is None:
            values.update({
                'pager': pager,
                'default_url': '/my/crm_lead',
                'crm_lead_ids': leads,
                # 'searchbar_sortings_2': searchbar_sortings
            })
            return request.render("website_crm_lead.portal_my_crm_lead",
                                  values)
        else:
            crm_lead_id = Crm_lead.sudo().browse(crm_lead_id)
            values.update({
                'crm_lead_id': crm_lead_id})
            return request.render(
                "website_crm_lead.portal_my_crm_lead_details", values)
