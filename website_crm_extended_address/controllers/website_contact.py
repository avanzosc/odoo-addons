
from odoo import http
from odoo.http import request


class websiteContact(http.Controller):

    @http.route('/contactus_getdata', type='http', auth="user", website=True)
    def websiteContactData(self):
        state_ids = request.env['res.country.state'].search([])
        country_ids = request.env['res.country'].search([])
        values = {'state_ids': state_ids,
                  'country_ids': country_ids}
        return http.request.render('website.contactus', values)
    
    @http.route('/contactus_send',
                 type='http', auth="user", website=True)
    def websiteContact(self, **kwargs):
        crm_lead_values={
            'contact_name': kwargs['contact_name'],
            'phone': kwargs['phone'],
            'email_from': kwargs['email_from'],
            'partner_name': kwargs['partner_name'],
            'sending_street': kwargs['sending_street'],
            'sending_city': kwargs['sending_city'],
            'sending_state_id': kwargs['sending_state_id'],
            'sending_zip': kwargs['sending_zip'],
            'sending_country_id': kwargs['sending_country_id'],
            'comercial_name': kwargs['comercial_name'],
            'billing_phone': kwargs['billing_phone'],
            'billing_email': kwargs['billing_email'],
            'name': kwargs['name'],
            'description': kwargs['description'],
            'mobile': kwargs['mobile'],
            'vat': kwargs['vat'],
            'street': kwargs['street'],
            'city': kwargs['city'],
            'state_id': kwargs['state_id'],
            'zip': kwargs['zip'],
            'country_id': kwargs['country_id'],
            'website': kwargs['website'],
            'sending_phone': kwargs['sending_phone'],
            'sending_email': kwargs['sending_email'],
                        }
        try:
            crm_lead = request.env['crm.lead'].sudo().create(crm_lead_values)
            if crm_lead:
                msg_text = 'OK. CRM Lead Created!'
            else:
                msg_text = 'ERROR. CRM Lead Not Created!'
            values = {
                'msg_text': msg_text,
                'crm_lead': crm_lead,}
            return http.request.render('website_crm_extended_address.Crm_extended_send_contactus_form', values)
        except:
            values = {
                'msg_text': 'ERROR. Something Wrong Occured!',
                'mail_text': 'ERROR. Something Wrong Occured!'}
            return http.request.render('website_crm_extended_address.Crm_extended_send_contactus_form', values)
        
            
        
    