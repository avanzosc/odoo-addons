# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPickingBatchDecaChange(models.Model):
    _name = "stock.picking.batch.deca.change"
    _description = "DeCA In-Route Change (Método A)"
    _order = "change_date desc, id desc"

    batch_id = fields.Many2one(
        comodel_name="stock.picking.batch",
        required=True,
        ondelete="cascade",
    )
    field_label = fields.Char(required=True)
    old_value = fields.Char()
    new_value = fields.Char(required=True)
    reason = fields.Char(
        required=True,
        help="Mandatory justification for the change, kept for traceability "
        "as required by the Resolución's Método A (ap. Quinto).",
    )
    change_date = fields.Datetime(required=True, default=fields.Datetime.now)
    user_id = fields.Many2one(
        "res.users", required=True, default=lambda self: self.env.user
    )
