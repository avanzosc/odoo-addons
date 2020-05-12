
from odoo.http import request
from odoo.addons.sale.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        partner_customers = request.env['res.partner'].search([
            ('user_id.partner_id', '=', partner.id)
            ])
        values.update({
            'partner_customers': partner_customers,
        })
        return values
