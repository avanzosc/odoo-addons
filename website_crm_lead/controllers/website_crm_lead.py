
from odoo import http, _
from odoo.http import request
from odoo.addons.account.controllers.portal import CustomerPortal

class PortalCrmLead(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalCrmLead, self)._prepare_portal_layout_values()
        partner_id = request.env.user.partner_id
        crm_lead_count = request.env['crm.lead'].search_count([('partner_id.user_id.partner_id','=',partner_id.id)])
        values['crm_lead_count'] = crm_lead_count
        return values
    
    @http.route(['/my/crm_lead', '/my/crm_lead/<int:crm_lead_id>'], type='http', auth="user", website=True)
    def portal_my_crm_lead(self, crm_lead_id=None):
        values = self._prepare_portal_layout_values()
        partner_id = request.env.user.partner_id
        crm_lead_ids = request.env['crm.lead'].search([('partner_id.user_id.partner_id','=',partner_id.id)])

        values.update({
            'crm_lead_ids': crm_lead_ids,
            'page_name': 'crm_lead',
        })
        if crm_lead_id == None:
            return request.render("website_crm_lead.portal_my_crm_lead", values)
        else:
            crm_lead_id = request.env['crm.lead'].search([('id', '=', crm_lead_id)])
            values.update({
                'crm_lead_id': crm_lead_id})
            return request.render("website_crm_lead.portal_my_crm_lead_details", values)
            
        