# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    accounting_date = fields.Datetime(default=fields.Datetime.now, copy=False)

    def action_view_inventory_adjustment(self):
        result = super().action_view_inventory_adjustment()
        result.setdefault("context", {})
        result["context"].update({"inventory_date": self.accounting_date})
        return result

    def action_state_to_in_progress(self):
        for rec in self.filtered("accounting_date"):
            rec.date = rec.accounting_date
        result = super().action_state_to_in_progress()
        for rec in self.filtered("accounting_date"):
            rec.stock_quant_ids.filtered(
                lambda quant, rec=rec: quant.current_inventory_id == rec
            ).write({"inventory_date": rec.accounting_date})
        return result

    def action_state_to_done(self):
        result = super().action_state_to_done()
        for rec in self.filtered("accounting_date"):
            rec.stock_move_ids.write({"date": rec.accounting_date})
            rec.stock_move_ids.mapped("move_id").write({"date": rec.accounting_date})
        return result
