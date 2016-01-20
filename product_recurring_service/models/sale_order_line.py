# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    recurring_service = fields.Boolean(
        string='Recurring Service', related='product_id.recurring_service')
