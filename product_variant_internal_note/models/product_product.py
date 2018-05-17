# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    internal_note = fields.Text(
        string='Internal Note', help='This note is for internal purpose only',
        translate=True)
