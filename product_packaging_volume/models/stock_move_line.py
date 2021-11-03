# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    packaging_id = fields.Many2one(
        string='Package Type', comodel_name='product.packaging',
        related='result_package_id.packaging_id', store=True)
    height = fields.Integer(
        string='Height', related='packaging_id.height', store=True)
    width = fields.Integer(
        string='Width', related='packaging_id.width', store=True)
    packaging_length = fields.Integer(
        string='Packaging Length', related='packaging_id.packaging_length',
        store=True)
    volume = fields.Float(
        string='Volume', related='packaging_id.volume', store=True)
