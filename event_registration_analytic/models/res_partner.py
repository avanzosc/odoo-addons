# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends('bank_ids')
    @api.multi
    def _compute_num_bank_accounts(self):
        for partner in self:
            partner.num_bank_accounts = len(partner.bank_ids)

    @api.depends('bank_ids', 'bank_ids.mandate_ids',
                 'bank_ids.mandate_ids.state')
    @api.multi
    def _compute_num_valid_mandates(self):
        for partner in self:
            partner.num_valid_mandates = len(
                partner.mapped('bank_ids.mandate_ids').filtered(
                    lambda l: l.state == 'valid'))

    @api.depends('invoice_ids')
    @api.multi
    def _compute_num_invoices(self):
        for partner in self:
            partner.num_invoices = len(partner.invoice_ids)

    parent_is_company = fields.Boolean(
        string='Parent is company', related='parent_id.is_company', store=True)
    parent_is_group = fields.Boolean(
        string='Parent is group', related='parent_id.is_group', store=True)
    num_bank_accounts = fields.Integer(
        string='# bank accounts', compute='_compute_num_bank_accounts',
        store=True)
    num_valid_mandates = fields.Integer(
        string='# valid mandates', compute='_compute_num_valid_mandates',
        store=True)
    num_invoices = fields.Integer(
        string='# invoices', compute='_compute_num_invoices', store=True)
    parent_num_bank_accounts = fields.Integer(
        string='# bank accounts', related='parent_id.num_bank_accounts',
        store=True)
    parent_num_valid_mandates = fields.Integer(
        string='# valid mandates', related='parent_id.num_valid_mandates',
        store=True)
    parent_num_invoices = fields.Integer(
        string='# invoices', related='parent_id.num_invoices', store=True)
