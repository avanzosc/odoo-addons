# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import calendar
from openerp import fields, models, api
from dateutil.relativedelta import relativedelta
from openerp.addons import decimal_precision as dp


class AccountAssetDepreciationLine(models.Model):

    _inherit = 'account.asset.depreciation.line'

    method_percentage = fields.Float(string='Method Percentage')

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
        return fields.Date.to_string(depr_date)

    @api.model
    def _compute_board_amount(
            self, asset, i, residual_amount, amount_to_depr,
            undone_dotation_number, posted_depreciation_line_ids, total_days,
            depreciation_date):
        wiz = self.env.context.get('wiz', False)
        dep_date = asset._get_real_depreciation_date(depreciation_date)
        if not wiz or asset.method_time != 'percentage':
            return super(AccountAssetAsset, self)._compute_board_amount(
                asset, i, residual_amount, amount_to_depr,
                undone_dotation_number, posted_depreciation_line_ids,
                total_days, depreciation_date)
        amount = 0
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
        # depreciation_date = fields.Datetime.from_string(asset.purchase_date)
        if not (asset.method_time == 'percentage' and wizard):
            return super(AccountAssetAsset,
                         self)._compute_board_undone_dotation_nb(
                asset, depreciation_date, total_days)
        number = 0
        percentage = 100.0
        while percentage >= 0:
            percentage2apply = asset.method_percentage
            dep_date = fields.Date.to_string(depreciation_date)
            if dep_date >= wizard.start_date and \
                    dep_date <= wizard.end_date:
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

    # @api.multi
    # def compute_depreciation_board(self):
    #     result = super(AccountAssetAsset, self).compute_depreciation_board()
    #     for asset in self.filtered(lambda x: x.method_time == 'number'):
    #         percen = round(100. / asset.method_number, 2)
    #         if asset.method_percentage != percen:
    #             asset.write({'method_percentage': percen,
    #                          'annual_percentage': percen})
    #             for line in asset.depreciation_line_ids:
    #                 new_amount = round((asset.purchase_value * percen) / 100,
    #                                    2)
    #                 line.write({'amount': new_amount,
    #                             'method_percentage': percen})
    #         max_line, lines = asset._get_lines_maxline_information()
    #         amount = sum(lines.mapped('amount'))
    #         max_line.write({'amount': asset.purchase_value - amount,
    #                         'depreciated_value': amount})
    #         previous_line = max(lines, key=lambda x: x.id)
    #         previous_line.remaining_value = max_line.amount
    #         for line in asset.depreciation_line_ids:
    #             line.method_percentage = round(
    #                 ((line.amount * 100) / line.asset_id.purchase_value), 2)
    #     for asset in self.filtered(
    #             lambda x: x.method_time in ('percentage', 'number')):
    #         max_line, lines = asset._get_lines_maxline_information()
    #         percentage = sum(lines.mapped('method_percentage'))
    #         new_percentage = round(100 - percentage, 2)
    #         max_line.with_context(
    #             no_calculate_porcentage=True).write({'method_percentage':
    #                                                  new_percentage})
    #         amount = round(
    #             (asset.purchase_value * asset.method_percentage) / 100, 2)
    #         if amount < max_line.amount:
    #             max_line.write(
    #                 {'amount': amount,
    #                  'remaining_value': max_line.amount - amount,
    #                  'method_percentage': asset.method_percentage})
    #             new_line = max_line.copy()
    #             new_date = fields.Date.from_string(
    #                 max_line.depreciation_date) + relativedelta(
    #                 months=asset.method_period)
    #             deprec_value = max_line.depreciated_value + max_line.amount
    #             new_line.write({'amount': max_line.remaining_value,
    #                             'remaining_value': 0.00,
    #                             'depreciation_date': new_date,
    #                             'depreciated_value': deprec_value})
    #             max_line = max(
    #                 asset.depreciation_line_ids, key=lambda x: x.id)
    #             lines = asset.depreciation_line_ids.filtered(
    #                 lambda x: x.id != max_line.id)
    #             perc = sum(lines.mapped('method_percentage'))
    #             i = len(asset.depreciation_line_ids) - 1
    #             asset.depreciation_line_ids[i].method_percentage = (100 -
    #                                                                 perc)
    #     return result
    #
    # @api.multi
    # def _get_lines_maxline_information(self):
    #     max_line = max(self.depreciation_line_ids, key=lambda x: x.id)
    #     lines = self.mapped(
    #         'depreciation_line_ids').filtered(lambda l: l.id < max_line.id)
    #     return max_line, lines
