# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.report import report_sxw
from openerp import models


class AccountAssetReport(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(AccountAssetReport, self).__init__(
            cr, uid, name, context=context)


class ReportAccountAsset(models.AbstractModel):
    _name = 'report.l10n_es_account_asset_variation.report_asset'
    _inherit = 'report.abstract_report'
    _template = 'l10n_es_account_asset_variation.report_asset'
    _wrapped_report_class = AccountAssetReport
