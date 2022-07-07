# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    batch_id = fields.Many2one(
        string='Mother',
        comodel_name='stock.picking.batch',
        domain="[('batch_type', '=', 'mother')]")
    requires_mother = fields.Boolean(
        string='Requires Mother',
        default=False,
        related='product_id.requires_mother',
        store=True)
