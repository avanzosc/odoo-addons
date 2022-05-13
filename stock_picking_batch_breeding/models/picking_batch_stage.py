# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class PickingBatchStage(models.Model):
    _inherit = "picking.batch.stage"

    batch_type = fields.Selection(
        string='Batch Type',
        selection_add=[("breeding", "Breeding")])
