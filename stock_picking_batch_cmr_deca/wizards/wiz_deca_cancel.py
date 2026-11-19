# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class WizDecaCancel(models.TransientModel):
    _name = "wiz.deca.cancel"
    _description = "Cancel a DeCA Before Its Service Starts"

    batch_id = fields.Many2one(comodel_name="stock.picking.batch", required=True)
    reason = fields.Char(required=True)

    def action_confirm(self):
        self.ensure_one()
        self.batch_id._deca_cancel(self.reason)
        return {"type": "ir.actions.act_window_close"}
