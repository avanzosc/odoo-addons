# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    def _compute_picking_count(self):
        for account in self:
            account.picking_count = len(account.picking_ids)

    picking_ids = fields.One2many(
        comodel_name="stock.picking", inverse_name='analytic_account_id',
        string='Pickings')
    picking_count = fields.Integer(
        string='Pickings', compute='_compute_picking_count')

    def show_pickings_from_analytic_account(self):
        res = {'view_mode': 'tree,kanban,form,calendar',
               'res_model': 'stock.picking',
               'view_id': False,
               'type': 'ir.actions.act_window',
               'view_type': 'form',
               'domain': [('id', 'in', self.picking_ids.ids)]}
        return res
