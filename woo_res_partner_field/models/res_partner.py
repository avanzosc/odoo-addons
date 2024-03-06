# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_from_woo = fields.Boolean(
        "Customer Imported from WooCommerce"
    )
    
    def woo_create_contact_customer():
        partners = super().woo_create_contact_customer()
        for partner in partners: 
            partner.customer_from_woo = True
        
        return partners