# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    custom_stock_planning_rule = fields.Boolean(
        string='Customize min. qty, and max. qty rules', default=False)
    stock_planning_min_days = fields.Integer(
        'Min. days', help='Days to calculate the minimum stock rule',
        default=0)
    stock_planning_max_days = fields.Integer(
        'Max. days', help='Days to calculate the maximum stock rule',
        default=0)

    @api.constrains('custom_stock_planning_rule',
                    'stock_planning_min_days', 'stock_planning_max_days')
    def _check_custom_stock_planning_rule(self):
        if self.custom_stock_planning_rule:
            if (self.stock_planning_min_days == 0 or
                    self.stock_planning_max_days == 0):
                raise exceptions.Warning(
                    _('You must enter the days to calculate stock planning'
                      ' rules'))
            if self.stock_planning_min_days >= self.stock_planning_max_days:
                raise exceptions.Warning(
                    _('Day minimum must be less than maximum days'))
