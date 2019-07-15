# -*- coding: utf-8 -*-
# © 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class StockQuant(models.Model):

    _inherit = 'stock.quant'

    pck_qty = fields.Integer(string='Package Qty to print', default=1)
    ul_id = fields.Many2one(comodel_name="product.ul", string="Logistic Unit")
