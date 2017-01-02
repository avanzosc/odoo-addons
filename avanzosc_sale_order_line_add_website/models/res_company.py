# -*- coding: utf-8 -*-
# © 2016 AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    parent_website = fields.Many2one(
        comodel_name='account.analytic.account', string='Parent Website')
    parent_product = fields.Many2one(
        comodel_name='account.analytic.account', string='Parent Product')
