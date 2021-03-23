# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    default_packaging_id = fields.Many2one('product.packaging', string='Default Packaging',
                                           related='product_id.categ_id.default_packaging_id')
