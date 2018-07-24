# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from dateutil.relativedelta import relativedelta


class AccountAssetVariation(models.TransientModel):

    _name = 'account.asset.variation'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    percentage = fields.Integer(string='Percentage', required=True)

    @api.multi
    def action_calculate_depreciation_board(self):
        self.ensure_one()
        asset_id = self.env.context.get('active_id')
        asset = self.env['account.asset.asset'].browse(asset_id)
        asset.with_context(wiz=self).compute_depreciation_board()
        if asset.depreciation_line_ids:
            max_line = max(asset.depreciation_line_ids, key=lambda x: x.id)
            amount = round(
                (asset.purchase_value * max_line.method_percentage) / 100, 2)
            if amount < max_line.amount:
                max_line.write({'amount': amount,
                                'remaining_value': max_line.amount - amount})
                new_line = max_line.copy()
                new_date = fields.Date.from_string(
                    max_line.depreciation_date) + relativedelta(
                    months=asset.method_period)
                deprec_value = max_line.depreciated_value + max_line.amount
                new_line.write({'amount': max_line.remaining_value,
                                'remaining_value': 0.00,
                                'depreciation_date': new_date,
                                'depreciated_value': deprec_value})
                max_line = max(asset.depreciation_line_ids, key=lambda x: x.id)
                lines = asset.depreciation_line_ids.filtered(
                    lambda x: x.id != max_line.id)
                perc = sum(lines.mapped('method_percentage'))
                i = len(asset.depreciation_line_ids) - 1
                asset.depreciation_line_ids[i].method_percentage = 100 - perc
        return True
