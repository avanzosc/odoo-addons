# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    contact_type_id = fields.Many2one(
        string='Contact type', comodel_name='res.partner.type',
        related='partner_id.contact_type_id', store=True)
    analytic_account_id = fields.Many2one(
        string='Analytic Account', comodel_name='account.analytic.account',
        compute='_compute_analytic_account_id', store=True, related=False,
        company_dependent=False)

    @api.depends('contact_type_id', 'contact_type_id.analytic_account_id')
    def _compute_analytic_account_id(self):
        for move in self.filtered(
            lambda x: x.contact_type_id and
                x.move_type in ('out_invoice', 'out_refund', 'out_receipt')):
            if (move.contact_type_id.with_company(
                    move.company_id.id).analytic_account_id):
                move.analytic_account_id = move.contact_type_id.with_company(
                    move.company_id.id).analytic_account_id.id
