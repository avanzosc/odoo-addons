# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    barcode_scanned = fields.Char(
        string="Barcode Scanned")

    @api.onchange('barcode_scanned')
    def onchange_barcode_scanned(self):
        lot_obj = self.env["stock.production.lot"]
        if self.barcode_scanned and self.product_id:
            if ("show_lots_m2o" in self.env.context and
                    self.env.context.get("show_lots_m2o", False)):
                cond = [("name", "=", self.barcode_scanned),
                        ("product_id", "=", self.product_id.id)]
                lot = lot_obj.search(cond, limit=1)
                if not lot:
                    raise ValidationError(
                       _("Lot: '{}', not found.").format(self.barcode_scanned))
                    self.barcode_scanned = ""
                self.lot_id = lot.id
            if ("show_lots_text" in self.env.context and
                    self.env.context.get("show_lots_text", False)):
                self.lot_name = self.barcode_scanned
