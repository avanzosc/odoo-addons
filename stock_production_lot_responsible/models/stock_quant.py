# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    ref = fields.Char(
        string='Internal Reference', related='lot_id.ref',
        store=True)
    responsible_id = fields.Many2one(
        string='Responsible', related='lot_id.responsible_id', store=True)
