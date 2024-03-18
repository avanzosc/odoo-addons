# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def preview_sale_order(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        result = super(SaleOrder, self).preview_sale_order()
        return result
