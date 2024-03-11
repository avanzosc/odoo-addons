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
    def woo_create_contact_customer(self):
        partner = super(ResPartner, self).woo_create_contact_customer()
        partner.write({'customer_from_woo': True})
        _logger.info("\n\ncustomer_from_woo written in partner: %s\n", partner.id)
        return partner
    
    @api.model
    def woo_create_or_update_customer(self):
        partner = super(ResPartner, self).woo_create_or_update_customer()
        partner.write({'customer_from_woo': True})
        _logger.info("\n\ncustomer_from_woo written in partner: %s\n", partner.id)
        return partner
