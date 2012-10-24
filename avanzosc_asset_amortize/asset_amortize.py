
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2012 Daniel (AvanzOSC). All Rights Reserved
#    
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import fields, osv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar

class account_asset_asset(osv.osv):
    
    _description = 'Asset'
    _inherit = 'account.asset.asset'
    
    _columns = {
                'percent': fields.integer('Percent of Depreciation', help="If the percent is more than 0, the depreciation will be used as percent."),
                'fiscal_pcnt': fields.integer('Fiscal Percent of Depreciation', help="If the percent is more than 0, the depreciation will be used as percent."),
                'fiscal_deprec_line_ids': fields.one2many('account.asset.fiscal.depreciation.line', 'asset_id', 'Depreciation Lines', readonly=True, states={'draft':[('readonly',False)],'open':[('readonly',False)]}),
                }
    
    def onchange_percent(self, cr, uid, ids, percent, context=None):
        values =  {}
        if percent > 0:
            years = 100 / percent
            month = 100 % percent
            values =  {'method_number' : years,
                       'method_period' : 12
                       }
        return {'value' :values}

    def compute_depreciation_board(self, cr, uid, ids, context=None):
        data = self.browse(cr, uid, ids[0], context=context)
        depreciation_lin_obj = self.pool.get('account.asset.depreciation.line')
        if data.percent <= 0 :
            super (account_asset_asset , self).compute_depreciation_board (cr, uid, ids, context)
        else:
            for asset in self.browse(cr, uid, ids, context=context):
                if asset.value_residual == 0.0:
                    continue
                posted_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_check', '=', True)])
                old_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_id', '=', False)])
                if old_depreciation_line_ids:
                    depreciation_lin_obj.unlink(cr, uid, old_depreciation_line_ids, context=context)
            
                amount_to_depr = residual_amount = asset.value_residual

                depreciation_date = datetime.strptime(self._get_last_depreciation_date(cr, uid, [asset.id], context)[asset.id], '%Y-%m-%d')
                day = depreciation_date.day
                month = depreciation_date.month
                year = depreciation_date.year
                total_days = (year % 4) and 365 or 366

                undone_dotation_number = self._compute_board_undone_dotation_nb(cr, uid, asset, depreciation_date, total_days, context=context)
                for x in range(len(posted_depreciation_line_ids), undone_dotation_number):
                    i = x + 1
                    amount_virt = self._compute_board_amount(cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=context)
                    amount = amount_virt
                    residual_amount -= amount
                    if asset.compute_at_end_period:
                        if asset.prorata and asset.method_period == 12:
                            depreciation_date = depreciation_date.replace(year, 12, 31)
                        else:
                            last_month_day = calendar.monthrange(year, month)[1]
                            depreciation_date = depreciation_date.replace(year, month, last_month_day)

                    vals = {
                            'amount': amount,
                            'asset_id': asset.id,
                            'sequence': i,
                            'name': str(asset.id) + '/' + str(i),
                            'remaining_value': residual_amount,
                            'depreciated_value': (asset.purchase_value - asset.salvage_value) - (residual_amount + amount),
                            'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),
                     }
                    depreciation_lin_obj.create(cr, uid, vals, context=context)
                    # Considering Depr. Period as months
                    depreciation_date = (datetime(year, month, day) + relativedelta(months= +asset.method_period))
                    day = depreciation_date.day
                    month = depreciation_date.month
                    year = depreciation_date.year
        return True
    
    def _compute_board_amount(self, cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=None):
        #by default amount = 0
        amount = 0
        if i == undone_dotation_number:
            amount = residual_amount
        else:
            percent = asset.percent
            if percent <= 0:
                amount = super(account_asset_asset , self)._compute_board_amount (cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=None)
            else :
                if asset.method == 'linear':
                    amount = amount_to_depr / (undone_dotation_number - len(posted_depreciation_line_ids))
                    if asset.prorata:
                        percent = asset.percent * 0.01
                        amount = amount_to_depr * percent
                        days = total_days - float(depreciation_date.strftime('%j'))
                        if i == 1:
                            amount = (amount_to_depr * asset.percent * 0.01) / total_days * days
                        elif i == undone_dotation_number:
                            amount = (amount_to_depr * asset.percent * 0.01) / total_days * (total_days - days)
        return amount
    
    def compute_fiscal_depreciation_board(self, cr, uid, ids, context=None):
        data = self.browse(cr, uid, ids[0], context=context)
        depreciation_lin_obj = self.pool.get('account.asset.fiscal.depreciation.line')
        if data.fiscal_pcnt <= 0 :
            for asset in self.browse(cr, uid, ids, context=context):
                if asset.value_residual == 0.0:
                    continue
                posted_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_check', '=', True)])
                old_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_id', '=', False)])
                if old_depreciation_line_ids:
                    depreciation_lin_obj.unlink(cr, uid, old_depreciation_line_ids, context=context)
            
                amount_to_depr = residual_amount = asset.value_residual

                depreciation_date = datetime.strptime(self._get_last_depreciation_date(cr, uid, [asset.id], context)[asset.id], '%Y-%m-%d')
                day = depreciation_date.day
                month = depreciation_date.month
                year = depreciation_date.year
                total_days = (year % 4) and 365 or 366

                undone_dotation_number = self._compute_board_undone_dotation_nb(cr, uid, asset, depreciation_date, total_days, context=context)
                for x in range(len(posted_depreciation_line_ids), undone_dotation_number):
                    i = x + 1
                    amount = self._compute_fiscal_board_amount(cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=context)
                    residual_amount -= amount
                    if asset.compute_at_end_period:
                        if asset.prorata and asset.method_period == 12:
                            depreciation_date = depreciation_date.replace(year, 12, 31)
                        else:
                            last_month_day = calendar.monthrange(year,month)[1]
                            depreciation_date = depreciation_date.replace(year, month, last_month_day)

                    vals = {
                            'amount': amount,
                            'asset_id': asset.id,
                            'sequence': i,
                            'name': str(asset.id) +'/' + str(i),
                            'remaining_value': residual_amount,
                            'depreciated_value': (asset.purchase_value - asset.salvage_value) - (residual_amount + amount),
                            'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),
                            }
                    depreciation_lin_obj.create(cr, uid, vals, context=context)
                    # Considering Depr. Period as months
                    depreciation_date = (datetime(year, month, day) + relativedelta(months=+asset.method_period))
                    day = depreciation_date.day
                    month = depreciation_date.month
                    year = depreciation_date.year
        else:
            for asset in self.browse(cr, uid, ids, context=context):
                if asset.value_residual == 0.0:
                    continue
                posted_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_check', '=', True)])
                old_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_id', '=', False)])
                if old_depreciation_line_ids:
                    depreciation_lin_obj.unlink(cr, uid, old_depreciation_line_ids, context=context)
            
                amount_to_depr = residual_amount = asset.value_residual

                depreciation_date = datetime.strptime(self._get_last_depreciation_date(cr, uid, [asset.id], context)[asset.id], '%Y-%m-%d')
                day = depreciation_date.day
                month = depreciation_date.month
                year = depreciation_date.year
                total_days = (year % 4) and 365 or 366

                undone_dotation_number = self._compute_board_undone_dotation_nb(cr, uid, asset, depreciation_date, total_days, context=context)
                for x in range(len(posted_depreciation_line_ids), undone_dotation_number):
                    i = x + 1
                    amount_virt = self._compute_fiscal_board_amount(cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=context)
                    amount = amount_virt
                    residual_amount -= amount
                    if asset.compute_at_end_period:
                        if asset.prorata and asset.method_period == 12:
                            depreciation_date = depreciation_date.replace(year, 12, 31)
                        else:
                            last_month_day = calendar.monthrange(year, month)[1]
                            depreciation_date = depreciation_date.replace(year, month, last_month_day)

                    vals = {
                            'amount': amount,
                            'asset_id': asset.id,
                            'sequence': i,
                            'name': str(asset.id) + '/' + str(i),
                            'remaining_value': residual_amount,
                            'depreciated_value': (asset.purchase_value - asset.salvage_value) - (residual_amount + amount),
                            'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),
                     }
                    depreciation_lin_obj.create(cr, uid, vals, context=context)
                    # Considering Depr. Period as months
                    depreciation_date = (datetime(year, month, day) + relativedelta(months= +asset.method_period))
                    day = depreciation_date.day
                    month = depreciation_date.month
                    year = depreciation_date.year
        return True
    
    def _compute_fiscal_board_amount(self, cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=None):
        #by default amount = 0
        amount = 0
        if i == undone_dotation_number:
            amount = residual_amount
        else:
            percent = asset.fiscal_pcnt
            if percent <= 0:                
                if asset.method == 'linear':
                    amount = amount_to_depr / (undone_dotation_number - len(posted_depreciation_line_ids))
                    if asset.prorata:
                        amount = amount_to_depr / asset.method_number
                        days = total_days - float(depreciation_date.strftime('%j'))
                        if i == 1:
                            amount = (amount_to_depr / asset.method_number) / total_days * days
                        elif i == undone_dotation_number:
                            amount = (amount_to_depr / asset.method_number) / total_days * (total_days - days)
                elif asset.method == 'degressive':
                    amount = residual_amount * asset.method_progress_factor
                    if asset.prorata:
                        days = total_days - float(depreciation_date.strftime('%j'))
                        if i == 1:
                            amount = (residual_amount * asset.method_progress_factor) / total_days * days
                        elif i == undone_dotation_number:
                            amount = (residual_amount * asset.method_progress_factor) / total_days * (total_days - days)
            else :
                if asset.method == 'linear':
                    amount = amount_to_depr / (undone_dotation_number - len(posted_depreciation_line_ids))
                    if asset.prorata:
                        percent = asset.fiscal_pcnt * 0.01
                        amount = amount_to_depr * percent
                        days = total_days - float(depreciation_date.strftime('%j'))
                        if i == 1:
                            amount = (amount_to_depr * asset.fiscal_pcnt * 0.01) / total_days * days
                        elif i == undone_dotation_number:
                            amount = (amount_to_depr * asset.fiscal_pcnt * 0.01) / total_days * (total_days - days)
                        
        return amount
    
account_asset_asset()

class account_asset_fiscal_depreciation_line(osv.osv):
    _name = 'account.asset.fiscal.depreciation.line'
    _inherit = 'account.asset.depreciation.line'
    _description = 'Asset depreciation line'

account_asset_fiscal_depreciation_line()


