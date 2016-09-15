# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class MrpProductionProductLine(models.Model):
    _inherit = 'mrp.production.product.line'

    @api.multi
    @api.depends('production_id.commercial_percent', 'subtotal',
                 'production_id.profit_percent')
    def _compute_profit_commercial(self):
        for mrp in self:
            mrp.profit = \
                mrp.subtotal * (mrp.production_id.profit_percent / 100)
            mrp.cost_total =\
                mrp.subtotal * ((100 + mrp.production_id.profit_percent) / 100)
            mrp.commercial = \
                (mrp.subtotal + mrp.profit) * \
                (mrp.production_id.commercial_percent / 100)

    profit = fields.Float(compute='_compute_profit_commercial')
    commercial = fields.Float(compute='_compute_profit_commercial')
