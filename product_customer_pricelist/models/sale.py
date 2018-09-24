# Copyright (c) 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if res:
            for order in self:
                pricelist = order.mapped(
                    'order_line.product_id.property_product_pricelist_id')
                if len(pricelist) == 1:
                    order.partner_id.property_product_pricelist = pricelist.id
        return res
