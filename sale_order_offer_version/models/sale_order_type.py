# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class SaleOrderType(models.Model):
    _inherit = 'sale.order.type'

    is_offer_type = fields.Boolean(
        string='It is an offer type', default=False)
