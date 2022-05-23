# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PickingBatchStage(models.Model):
    _name = "picking.batch.stage"
    _description = "Picking Batch Stage"
    _order = "sequence"

    name = fields.Char(
        string="Name",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
    )
    batch_type = fields.Selection(
        string="Batch Type",
        selection=[("other", "Other")],
    )

    _sql_constraints = [
        ("name_unique", "unique(name)", "Picking Batch Stage name already exists"),
    ]
