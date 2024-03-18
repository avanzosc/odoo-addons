# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    @api.onchange('type_id')
    def onchange_type_id(self):
        result = super(SaleOrder, self).onchange_type_id()
        for order in self:
            if order.type_id and order.type_id.carrier_id:
                order.carrier_id = order.type_id.carrier_id.id
        return result
