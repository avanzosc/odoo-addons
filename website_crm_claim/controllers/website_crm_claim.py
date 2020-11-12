
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalCrmClaim(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalCrmClaim, self)._prepare_portal_layout_values()
        partner_and_claims = self.get_partners_by_connected_user(
            'crm.claim')
        values.update({
            'crm_claim_partner_ids': list(set(partner_and_claims['partners'])),
            'crm_claim_count': len(partner_and_claims['model_objs']),
            'crm_claim_ids': partner_and_claims['model_objs'],
            'page_name': 'crm_claim',
        })
        return values

    @http.route(['/my/crm_claim', '/my/crm_claim/<int:crm_claim_id>',
                 '/my/crm_claim/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_crm_claim(self, crm_claim_id=None, page=1,
                            sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Crm_claim = request.env['crm.claim']
        # searchbar_sortings = self.get_query_order(sortby)
        filtered_claim = self.filter_data([], 'crm.claim', **kw)
        filtered_claim_ids = []
        for claim in filtered_claim:
            if claim in values['crm_claim_ids']:
                filtered_claim_ids.append(claim.id)
        domain = [('id', 'in', filtered_claim_ids)]
        claim_count = Crm_claim.sudo().search_count(domain)
        pager = portal_pager(
            url="/my/crm_claim",
            total=claim_count,
            page=page,
            step=self._items_per_page
        )
        pager = self.recalculatePager(pager, **kw)
        claims = Crm_claim.sudo().search(
            domain, limit=self._items_per_page,
            offset=pager['offset'])
        if crm_claim_id is None:
            values.update({
                'pager': pager,
                'default_url': '/my/crm_claim',
                'crm_claim_ids': claims,
                # 'searchbar_sortings_2': searchbar_sortings
            })
            return request.render("website_crm_claim.portal_my_crm_claim",
                                  values)
        else:
            crm_claim_id = Crm_claim.sudo().browse(crm_claim_id)
            values.update({
                'crm_claim_id': crm_claim_id})
            return request.render(
                "website_crm_claim.portal_my_crm_claim_details", values)
