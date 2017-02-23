# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order', string="Sale order")


class PurchaseRequisitionLine(models.Model):
    _inherit = 'purchase.requisition.line'

    sale_order_line_id = fields.Many2one(
        comodel_name='sale.order.line', string="Sale order line")
