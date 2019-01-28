# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import tools
from odoo import api, fields, models


class CrossoveredBudgetSummary(models.Model):
    _name = 'crossovered.budget.summary'
    _description = 'Crossovered Budget Summary Lines'
    _auto = False
    _rec_name = 'crossovered_budget_id'

    crossovered_budget_id = fields.Many2one(
        comodel_name='crossovered.budget', string='Budget')
    general_budget_id = fields.Many2one(
        comodel_name='account.budget.post', string='Budget Position')
    planned_amount = fields.Float(string='Planned Amount')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
        CREATE or REPLACE VIEW %s as (
            SELECT
              row_number() OVER () AS id,
              crossovered_budget_id,
              general_budget_id,
              SUM(planned_amount) as planned_amount
            FROM
              crossovered_budget_lines
            GROUP BY
              crossovered_budget_id,
              general_budget_id
        )""" % (
            self._table))
