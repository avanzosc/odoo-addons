# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    planned_percentage = fields.Float(string="Planned percentage (%)")
    probability_percentage = fields.Float(
        string="Probability percentage (%)", readonly=True,
        compute='_compute_probability_percentage')

    @api.one
    @api.depends('planned_percentage', 'amount_untaxed')
    def _compute_probability_percentage(self):
        self.probability_percentage = (self.planned_percentage *
                                       self.amount_untaxed)
