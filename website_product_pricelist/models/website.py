
from odoo import models
from odoo.http import request


class Website(models.Model):
    _inherit = 'website'

    def _get_pricelist_available(self, req, show_visible=False):
        res = super(Website, self)._get_pricelist_available(req, show_visible)

        if request.env.user.id == request.env.ref('base.public_user').id:
            return res

        partner = self.env.user.partner_id
        pricelists = partner.property_product_pricelist.id

        return self.env['product.pricelist'].browse(pricelists)
