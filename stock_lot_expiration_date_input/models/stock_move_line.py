# Copyright 2025 Ane Gurruchaga- AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    manual_expiration_date = fields.Datetime(
        string="Expiration Date Manual",
    )

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines.filtered(lambda x: x.lot_id):
            if line.manual_expiration_date:
                line.lot_id.expiration_date = line.manual_expiration_date
        return lines

    def write(self, vals):
        result = super().write(vals)
        if "lot_id" in vals:
            for line in self.filtered(lambda x: x.lot_id):
                if line.manual_expiration_date:
                    line.lot_id.expiration_date = line.manual_expiration_date

        return result

    def _action_done(self):
        result = super()._action_done()
        for line in self.filtered(lambda x: x.lot_id):
            if line.manual_expiration_date:
                line.lot_id.expiration_date = line.manual_expiration_date
        return result
