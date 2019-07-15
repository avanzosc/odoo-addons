# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class AnalyticEntriesReport(models.Model):
    _inherit = "analytic.entries.report"

    headquarters_id = fields.Many2one(
        comodel_name='res.headquarters', string='Headquarter')
    product_categ_id = fields.Many2one(
        string="Product category", comodel_name='product.category')

    def _select(self):
        select_str = super(AnalyticEntriesReport, self)._select()
        select_str += """, a.product_categ_id as product_categ_id,
                          a.headquarters_id as headquarters_id """
        return select_str

    def _group_by(self):
        group_by_str = super(AnalyticEntriesReport, self)._group_by()
        group_by_str += """,a.product_categ_id, a.headquarters_id """
        return group_by_str
