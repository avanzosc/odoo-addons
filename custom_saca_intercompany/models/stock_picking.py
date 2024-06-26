# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    saca_line_id = fields.Many2one(
        string="Saca Line",
        comodel_name="saca.line",
        compute="_compute_saca_line_id",
        store=True,
    )
    saca_id = fields.Many2one(
        string="Saca", comodel_name="saca", related="saca_line_id.saca_id", store=True
    )
    tolvasa = fields.Boolean(string="Tolvasa", related="company_id.tolvasa", store=True)
    paasa = fields.Boolean(string="Paasa", related="company_id.paasa", store=True)

    @api.depends(
        "sale_id", "sale_id.saca_line_id", "purchase_id", "purchase_id.saca_line_id"
    )
    def _compute_saca_line_id(self):
        for line in self:
            line.saca_line_id = False
            if line.sale_id and line.sale_id.saca_line_id:
                line.saca_line_id = line.sale_id.saca_line_id.id
            elif line.purchase_id and line.purchase_id.saca_line_id:
                line.saca_line_id = line.purchase_id.saca_line_id.id

    def button_validate(self):
        result = super().button_validate()
        for picking in self:
            if (
                not picking.company_id.tolvasa
                and picking.sale_id
                and (picking.sale_id.auto_purchase_order_id)
                and (picking.state == "done")
            ):
                purchase_picking = (
                    picking.sale_id.sudo().auto_purchase_order_id.picking_ids.filtered(
                        lambda c: c.state not in ("cancel", "done")
                    )[:1]
                )
                if purchase_picking:
                    purchase_picking.button_force_done_detailed_operations()
                    for line in picking.move_line_ids_without_package.filtered(
                        lambda c: (c.lot_id)
                    ):
                        if not purchase_picking.move_line_ids_without_package.filtered(
                            lambda c: c.product_id == line.product_id
                            and c.lot_id == line.lot_id
                        ):
                            purchase_line = (
                                purchase_picking.move_line_ids_without_package.filtered(
                                    lambda c: c.product_id == line.product_id
                                    and not c.lot_id
                                )
                            )
                            if not purchase_line:
                                purchase_line = (
                                    self.env["stock.move.line"]
                                    .sudo()
                                    .create(
                                        {
                                            "product_id": line.product_id.id,
                                            "product_uom_id": (
                                                line.product_id.uom_id.id
                                            ),
                                            "qty_done": line.qty_done,
                                            "picking_id": purchase_picking.id,
                                            "location_id": (
                                                purchase_picking.location_id.id
                                            ),
                                            "location_dest_id": purchase_picking.location_dest_id.id,
                                        }
                                    )
                                )
                            lot = (
                                self.env["stock.production.lot"]
                                .sudo()
                                .search(
                                    [
                                        ("name", "=", line.lot_id.name),
                                        (
                                            "company_id",
                                            "=",
                                            purchase_picking.company_id.id,
                                        ),
                                        ("product_id", "=", line.product_id.id),
                                    ],
                                    limit=1,
                                )
                            )
                            if not lot:
                                lot = (
                                    self.env["stock.production.lot"]
                                    .sudo()
                                    .create(
                                        {
                                            "name": line.lot_id.name,
                                            "company_id": (
                                                purchase_picking.company_id.id
                                            ),
                                            "product_id": (line.product_id.id),
                                        }
                                    )
                                )
                            purchase_line.lot_id = lot.id
                            purchase_line.qty_done = line.qty_done
        return result
