# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class PickingBatchStage(models.Model):
    _name = "picking.batch.stage"
    _description = "Picking Batch Stage"

    name = fields.Char(string='Name')
