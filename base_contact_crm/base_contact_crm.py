from osv import osv, fields


class base_contact_crm_case(osv.osv):
    _inherit = 'crm.lead'

    _columns = {
        'partner_address_id': fields.many2one('res.partner.address', 'Partner Contact', domain="[('partner_id','=',partner_id)]"),
	'contact_id' : fields.many2one('res.partner.contact', 'Contact'),
    }

    def on_change_contact_id(self, cr, uid, ids, contact_id, context=None):
        if not contact_id:
            return {'value': {'partner_address_id': ''}}

        contact = self.pool.get('res.partner.contact').browse(cr, uid, [contact_id])[0]
        if contact.job_ids and contact.job_ids[0].address_id:
            return {'value' : {'partner_address_id' : contact.job_ids[0].address_id.id }}

        return {'value' : {}}

base_contact_crm_case()
