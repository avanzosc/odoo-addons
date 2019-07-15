# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    _order = 'price_unit'

    prequisition_line_id = fields.Many2one(
        comodel_name='purchase.requisition.line',
        string='Purchase requisition line')
    total_amount_used = fields.Boolean(
        string='Total amount used', default=False)
    partial_amount_used = fields.Boolean(
        string='Partial amount used', default=False)
