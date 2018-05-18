# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tools.safe_eval import safe_eval
from odoo import api, fields, models
from odoo.osv import expression


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _compute_assets_count(self):
        for invoice in self:
            cond = [('invoice_id', '=', invoice.id)]
            invoice.assets_count = (
                self.env['account.asset.asset'].search_count(cond))

    assets_count = fields.Integer(
        string='Assets', compute='_compute_assets_count')

    def show_assets_from_invoice(self):
        res = {}
        if self.assets_count:
            action = self.env.ref(
                'account_asset.action_account_asset_asset_form')
            action_dict = action.read()[0] if action else {}
            new_domain = [('invoice_id', '=', self.id)]
            action_dict['domain'] = expression.AND(
                [new_domain, safe_eval(action_dict.get('domain', '[]'))])
            return action_dict
        return res


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    account_asset_ids = fields.One2many(
        comodel_name='account.asset.asset', string='Assets',
        inverse_name='invoice_line_id')

    @api.one
    def asset_create(self):
        return super(AccountInvoiceLine,
                     self.with_context(
                         default_invoice_line_id=self.id)).asset_create()
