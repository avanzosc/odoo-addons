# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class StockTransferDetailsItems(models.TransientModel):
    _inherit = 'stock.transfer_details_items'

    percentage = fields.Integer(string='Percentage',
                                related='lot_id.percentage')
    unit_price = fields.Float(string='Price Unit', related='lot_id.unit_price')
