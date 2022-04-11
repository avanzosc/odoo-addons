# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    def _compute_picking_count(self):
        for account in self:
            account.picking_count = len(account.picking_ids)

    picking_ids = fields.One2many(
        comodel_name='stock.picking', inverse_name='analytic_account_id',
        string='Pickings')
    picking_count = fields.Integer(
        string='Picking Count', compute='_compute_picking_count')

    def show_pickings_from_analytic_account(self):
        action = self.env.ref('stock.action_picking_tree_all')
        action_dict = action.read()[0]
        action_dict.update({
            'domain': [('analytic_account_id', 'in', self.ids)],
        })
        return action_dict
