# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    location_id = fields.Many2one(
        string='Location',
        comodel_name='stock.location')
    batch_type = fields.Selection(
        string='Batch Type', selection=[("other", "Other")], default="other")
    warehouse_id = fields.Many2one(
        string='Farm',
        comodel_name='stock.warehouse',
        related='location_id.warehouse_id',
        store=True)
    partner_id = fields.Many2one(
        string='Owner',
        comodel_name='res.partner',
        related='location_id.warehouse_id.partner_id',
        store=True)
    stage_id = fields.Many2one(
        string='Stage',
        comodel_name="picking.batch.stage",
        copy=False)
