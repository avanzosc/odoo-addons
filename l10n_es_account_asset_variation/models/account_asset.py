# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import calendar
from openerp import fields, models, api
from dateutil.relativedelta import relativedelta
from openerp.addons import decimal_precision as dp

date2string = fields.Date.to_string


class AccountAssetDepreciationLine(models.Model):

    _inherit = 'account.asset.depreciation.line'

    method_percentage = fields.Float(
        string='Method Percentage', digits=dp.get_precision('Discount'))
    depreciated_value = fields.Float(digits=dp.get_precision('Account'))

    @api.multi
    def write(self, values):
        wiz = self.env.context.get('wiz', False)
        if not wiz:
            return super(AccountAssetDepreciationLine, self).write(values)
        if 'depreciation_date' not in values:
            return True
        for record in self.filtered(lambda x: x.asset_id.method_time ==
                                    'percentage'):
            percentage = record.asset_id.method_percentage
            dep_date = values.get('depreciation_date')
            if (wiz and dep_date >= wiz.start_date and
                    dep_date <= wiz.end_date):
                percentage = wiz.percentage
            values['method_percentage'] = percentage
            super(AccountAssetDepreciationLine, record).write(values)

    @api.model
    def create(self, values):
        wiz = self.env.context.get('wiz', False)
        asset = self.env['account.asset.asset'].browse(values.get('asset_id'))
        if asset.method_time == 'percentage' and 'depreciation_date' in values:
            percentage = asset.method_percentage
            dep_date = values.get('depreciation_date')
            if wiz and dep_date >= wiz.start_date and dep_date <= wiz.end_date:
                percentage = wiz.percentage
            values.update({'method_percentage': percentage})
        return super(AccountAssetDepreciationLine, self).create(values)


class AccountAssetAsset(models.Model):

    _inherit = 'account.asset.asset'

    @api.multi
    @api.depends('code', 'company_id')
    def _compute_invoice_id(self):
        invoice_obj = self.env['account.invoice']
        for record in self.filtered(lambda x: x.code):
            invoice = invoice_obj.search(
                [('number', '=', record.code), ('type', '=', 'in_invoice'),
                 ('company_id', '=', record.company_id.id)], limit=1)
            record.invoice_id = invoice

    @api.multi
    @api.depends('depreciation_line_ids', 'depreciation_line_ids.move_id',
                 'depreciation_line_ids.amount')
    def _amount_residual(self):
        for record in self:
            done_amount = sum(
                record.depreciation_line_ids.filtered(lambda x: x.move_id
                                                      ).mapped('amount'))
            record.value_residual = record.purchase_value - done_amount

    invoice_id = fields.Many2one(comodel_name='account.invoice',
                                 string='Invoice', store=True,
                                 compute='_compute_invoice_id')
    value_residual = fields.Float(string='Residual Value',
                                  compute='_amount_residual',
                                  digits=dp.get_precision('Account'))
    sequence = fields.Char(string='Code', default='/', copy=False)
    drop_date = fields.Date(string='Drop date')
    drop_reason = fields.Char(string="Drop reason")

    @api.multi
    def _get_last_depreciation_date(self):
        res = {}
        for record in self:
            done_lines = record.depreciation_line_ids.filtered(lambda x:
                                                               x.move_id)
            date = max([record.purchase_date] +
                       done_lines.mapped('depreciation_date'))
            max_date = fields.Date.from_string(date)
            if done_lines and record.prorata:
                max_date = (max_date +
                            relativedelta(months=+record.method_period))
            res[record.id] = fields.Date.to_string(max_date)
        return res

    @api.multi
    def _get_real_depreciation_date(self, depr_date):
        self.ensure_one()
        if self.method_period == 12:
            depr_date = depr_date.replace(depr_date.year, 12, 31)
        return depr_date

    @api.model
    def _compute_board_amount(
            self, asset, i, residual_amount, amount_to_depr,
            undone_dotation_number, posted_depreciation_line_ids, total_days,
            depreciation_date):
        wiz = self.env.context.get('wiz', False)
        dep_date = date2string(asset._get_real_depreciation_date(
            depreciation_date))
        if not wiz or asset.method_time != 'percentage':
            return super(AccountAssetAsset, self)._compute_board_amount(
                asset, i, residual_amount, amount_to_depr,
                undone_dotation_number, posted_depreciation_line_ids,
                total_days, depreciation_date)
        if i == undone_dotation_number:
            amount = residual_amount
        else:
            percentage2apply = asset.method_percentage
            if dep_date >= wiz.start_date and dep_date <= wiz.end_date:
                percentage2apply = wiz.percentage
            if i == 1 and asset.prorata:
                if asset.method_period == 1:
                    total_days = calendar.monthrange(
                        depreciation_date.year, depreciation_date.month)[1]
                    days = total_days - float(depreciation_date.day) + 1
                else:
                    days = (total_days - float(
                        depreciation_date.strftime('%j'))) + 1
                percentage = percentage2apply * days / total_days
            else:
                percentage = percentage2apply
            amount = asset.purchase_value * percentage / 100
        return amount

    @api.model
    def _compute_board_undone_dotation_nb(self, asset, depreciation_date,
                                          total_days):
        wizard = self.env.context.get('wiz', False)
        depreciation_date = asset._get_real_depreciation_date(
            depreciation_date)
        if not (asset.method_time == 'percentage' and wizard):
            return super(AccountAssetAsset,
                         self)._compute_board_undone_dotation_nb(
                asset, depreciation_date, total_days)
        number = 0
        percentage = 100.0
        while percentage >= 0:
            percentage2apply = asset.method_percentage
            dep_date = date2string(depreciation_date)
            if dep_date >= wizard.start_date and dep_date <= wizard.end_date:
                percentage2apply = wizard.percentage
            if number == 0 and asset.prorata:
                days = (total_days -
                        float(depreciation_date.strftime('%j'))) + 1
                percentage -= percentage2apply * days / total_days
            else:
                percentage -= percentage2apply
            number += 1
            depreciation_date += relativedelta(months=+asset.method_period)
        return number

    @api.model
    def create(self, values):
        if values.get('sequence', '/') == '/':
            values['sequence'] = self.env['ir.sequence'].next_by_id(
                self.env.ref('l10n_es_account_asset_variation.'
                             'account_asset_sequence').id)
        return super(AccountAssetAsset, self).create(values)

    @api.one
    def copy(self, default=None):
        if default is None:
            default = {}
        default.setdefault('sequence', self.env['ir.sequence'].next_by_id(
            self.env.ref('l10n_es_account_asset_variation.'
                         'account_asset_sequence').id))
        return super(AccountAssetAsset, self).copy(default)
