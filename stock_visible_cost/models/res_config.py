# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields


class StockConfigSettings(models.TransientModel):
    _inherit = 'stock.config.settings'

    group_stock_visible_cost = fields.Boolean(
        string='Make visible costs in stock',
        implied_group='stock_visible_cost.group_visible_cost',
        help='Checking this will show cost in some stock objects')
