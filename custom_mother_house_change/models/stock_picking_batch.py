# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import ValidationError


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    def button_change_house(self):
        self.ensure_one()
        if not self.picking_ids:
            raise ValidationError(
                _("This batch has no any transfer."))
        wiz_obj = self.env["batch.house.change.wizard"]
        wiz = wiz_obj.with_context({
            "active_id": self.id,
            "active_model": "stock.picking.batch"}).create({})
        context = self.env.context.copy()
        context.update({
            "active_id": self.id,
            "active_model": "stock.picking.batch",
            })
        return {"name": _("House Change"),
                "type": "ir.actions.act_window",
                "res_model": "batch.house.change.wizard",
                "view_type": "form",
                "view_mode": "form",
                "res_id": wiz.id,
                "target": "new",
                "context": context}
