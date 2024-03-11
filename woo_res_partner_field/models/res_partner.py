# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_from_woo = fields.Boolean(
        "Customer Imported from WooCommerce"
    )
    
    @api.model
    def woo_create_contact_customer(self, vals, instance=False):
        partner = super(ResPartner, self).woo_create_contact_customer(vals, instance)
        partner.write({'customer_from_woo': True})
        _logger.info("\n\ncustomer_from_woo written in partner: %s woo_create_contact_customer\n", partner.id)
        return partner
    
    @api.model
    def woo_create_or_update_customer(self, customer_val, instance, parent_id, partner_type, customer_id=False):
        partner = super(ResPartner, self).woo_create_or_update_customer(customer_val, instance, parent_id, partner_type, customer_id)
        partner.write({'customer_from_woo': True})
        _logger.info("\n\ncustomer_from_woo written in partner: %s woo_create_or_update_customer\n", partner.id)
        return partner
