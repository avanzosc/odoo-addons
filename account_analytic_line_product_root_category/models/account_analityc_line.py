# -*- coding: utf-8 -*-
# © Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    product_root_category = fields.Many2one(
        comodel_name='product.category', compute='_compute_get_root_category',
        store=True, string="Root category")

    def _get_root_category(self, category):
        if not category.parent_id:
            return category
        else:
            return self._get_root_category(category.parent_id)

    @api.depends('product_id')
    def _compute_get_root_category(self):
        for line in self:
            line.product_root_category = line._get_root_category(
                line.product_id.categ_id)
