# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def action_change_location(self, location, quants):
        picking_import = self.env["stock.picking.import"].create(
            {
                "company_id": self.env.company.id,
                "file_date": fields.Date.today(),
                "filename": _("Change Location"),
            }
        )
        for quant in quants:
            quant = self.env["stock.quant"].search([("id", "=", quant)], limit=1)
            if quant.quantity > 0:
                picking_import.import_line_ids = [
                    (
                        0,
                        0,
                        {
                            "picking_location": quant.location_id.complete_name,
                            "picking_location_id": quant.location_id.id,
                            "picking_location_dest": location.complete_name,
                            "picking_location_dest_id": location.id,
                            "picking_owner": quant.owner_id.name,
                            "picking_owner_id": quant.owner_id.id,
                            "picking_product_id": quant.product_id.id,
                            "picking_lot": quant.lot_id.name,
                            "picking_lot_id": quant.lot_id.id,
                            "picking_qty_done": quant.quantity,
                        },
                    )
                ]
        picking_import.action_validate()
        if picking_import.state == "pass":
            picking_import.action_process()
        for picking in picking_import.import_line_ids.picking_id:
            picking.button_validate()
        return {
            "name": _("Change Location"),
            "domain": [],
            "res_model": "stock.picking.import",
            "res_id": picking_import.id,
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "view_type": "form",
            "target": "current",
        }
