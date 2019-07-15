# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    @api.depends('project_ids', 'project_ids.members',
                 'project_ids.message_follower_ids')
    def _compute_partner_ids(self):
        for account in self.filtered('project_ids'):
            projects = account.project_ids.filtered(
                lambda x: x.privacy_visibility == 'followers')
            partners = projects.mapped('members.partner_id') | \
                projects.mapped('message_follower_ids')
            account.partner_ids = [(6, 0, partners.ids)]

    partner_ids = fields.Many2many(
        comodel_name='res.partner', relation='partner_analytic_account_rel',
        column1='partner_id', column2='analytic_id', string='Partners',
        compute='_compute_partner_ids', store=True)
