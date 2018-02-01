# -*- coding: utf-8 -*-
# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _compute_assets_count(self):
        for invoice in self:
            cond = [('invoice_id', '=', invoice.id)]
            invoice.assets_count = len(
                self.env['account.asset.asset'].search(cond))

    assets_count = fields.Integer(
        string='Assets', compute='_compute_assets_count')

    def show_assets_from_invoice(self):
        res = {}
        if self.assets_count > 0:
            cond = [('invoice_id', '=', self.id)]
            lines = self.env['account.asset.asset'].search(cond)
            res = {'view_mode': 'tree,kanban,form',
                   'res_model': 'account.asset.asset',
                   'view_id': False,
                   'type': 'ir.actions.act_window',
                   'view_type': 'form',
                   'domain': [('id', 'in', lines.ids)]}
        return res


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    account_asset_ids = fields.One2many(
        comodel_name="account.asset.asset", string='Assets',
        inverse_name='invoice_line_id')

    @api.one
    def asset_create(self):
        return super(AccountInvoiceLine,
                     self.with_context(invoice_line_id=self.id)).asset_create()
