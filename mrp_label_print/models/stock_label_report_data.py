# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class StockLabelReportData(models.Model):

    _inherit = 'stock.label.report.data'

    production_id = fields.Many2one(comodel_name='mrp.production',
                                    string='Production')
