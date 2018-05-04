# -*- coding: utf-8 -*-
# Copyright 2018 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    product_categ_id = fields.Many2one(
        string="Product category", related="product_id.categ_id",
        store=True)
