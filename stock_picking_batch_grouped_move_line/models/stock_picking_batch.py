# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    grouped_move_line_ids = fields.Many2many(
        comodel_name="stock.picking.batch.grouped.move.line",
        relation="rel_picking_batch_move_grouped",
        column1="batch_id",
        column2="grouped_move_line_id",
        copy=False,
        string="Detailed operations grouped",
    )

    @api.depends("picking_ids", "picking_ids.state")
    def _compute_state(self):
        result = super()._compute_state()
        self._compute_stock_move_line_grouped()
        return result

    def _compute_stock_move_line_grouped(self):
        grouped_obj = self.env["stock.picking.batch.grouped.move.line"]
        for batch in self:
            grouped = grouped_obj
            if batch.grouped_move_line_ids:
                batch.grouped_move_line_ids.unlink()
            lines = {}
            for ope in batch.move_line_ids.filtered(
                lambda x: x.product_id and x.location_id and x.location_dest_id
            ):
                key = "{}-{}-{} ".format(
                    ope.product_id.id, ope.location_id.id, ope.location_dest_id.id
                )
                if key not in lines:
                    pickings = ope.picking_id.name if ope.picking_id else ""
                    packages = ope.package_id.name if ope.package_id else ""
                    lots = ope.lot_id.name if ope.lot_id else ""
                    owners = ope.owner_id.name if ope.owner_id else ""
                    result_packages = (
                        ope.result_package_id.name if ope.result_package_id else ""
                    )
                    vals = {
                        "pickings": pickings,
                        "packages": packages,
                        "product_id": ope.product_id.id,
                        "lots": lots,
                        "owners": owners,
                        "qty_done": ope.qty_done,
                        "location_id": ope.location_id.id,
                        "location_dest_id": ope.location_dest_id.id,
                        "result_packages": result_packages,
                    }
                    lines[key] = vals
                else:
                    qty_done = lines[key].get("qty_done") + ope.qty_done
                    pickings = lines[key].get("pickings")
                    packages = lines[key].get("packages")
                    lots = lines[key].get("lots")
                    owners = lines[key].get("owners")
                    result_packages = lines[key].get("result_packages")
                    if ope.picking_id and ope.picking_id.name not in pickings:
                        pickings = (
                            "{}, {}".format(pickings, ope.picking_id.name)
                            if pickings
                            else ope.picking_id.name
                        )
                    if ope.package_id and ope.package_id.name not in packages:
                        packages = (
                            "{}, {}".format(packages, ope.package_id.name)
                            if packages
                            else ope.package_id.name
                        )
                    if ope.lot_id and ope.lot_id.name not in lots:
                        lots = (
                            "{}, {}".format(lots, ope.lot_id.name)
                            if lots
                            else ope.lot_id.name
                        )
                    if ope.owner_id and ope.owner_id.name not in owners:
                        owners = (
                            "{}, {}".format(owners, ope.owner_id.name)
                            if owners
                            else ope.owner_id.name
                        )
                    if (
                        ope.result_package_id
                        and ope.result_package_id.name not in result_packages
                    ):
                        result_packages = (
                            "{}, {}".format(result_packages, ope.result_package_id.name)
                            if result_packages
                            else ope.result_package_id.name
                        )
                    lines[key]["pickings"] = pickings
                    lines[key]["packages"] = packages
                    lines[key]["lots"] = lots
                    lines[key]["owners"] = owners
                    lines[key]["qty_done"] = qty_done
                    lines[key]["result_packages"] = result_packages
            for key, val in lines.items():
                grouped += grouped_obj.create(val)
            if grouped:
                batch.grouped_move_line_ids = [(6, 0, grouped.ids)]
