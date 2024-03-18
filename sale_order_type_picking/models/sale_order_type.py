# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class SaleOrderType(models.Model):
    _inherit = 'sale.order.type'

    picking_type_id = fields.Many2one(
        string='Type operation', comodel_name='stock.picking.type')
    carrier_id = fields.Many2one(
        string='Delivery method', comodel_name='delivery.carrier')