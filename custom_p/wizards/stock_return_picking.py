# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    def _create_returns(self):
        new_picking, picking_type_id = super()._create_returns()
        return_picking = self.env["stock.picking"].browse(new_picking)
        if self.picking_id.intercompany_picking_id:
            intercomp_picking = self.picking_id.sudo().intercompany_picking_id
            picking = (
                self.env["stock.picking"]
                .sudo()
                .create(
                    {
                        "partner_id": intercomp_picking.partner_id.id,
                        "picking_type_id": (
                            intercomp_picking.picking_type_id.return_picking_type_id.id
                        ),
                        "location_id": intercomp_picking.location_dest_id.with_company(
                            intercomp_picking.company_id.id
                        ).id,
                        "location_dest_id": intercomp_picking.location_id.with_company(
                            intercomp_picking.company_id.id
                        ).id,
                        "company_id": intercomp_picking.company_id.id,
                        "group_id": intercomp_picking.group_id.id,
                    }
                )
            )
            if intercomp_picking.purchase_id:
                for line in intercomp_picking.move_line_ids_without_package:
                    move = (
                        self.env["stock.move"]
                        .sudo()
                        .create(
                            {
                                "purchase_line_id": line.move_id.purchase_line_id.id,
                                "picking_id": picking.id,
                                "product_id": line.product_id.id,
                                "name": line.move_id.name,
                                "product_uom": line.product_uom_id.id,
                                "product_uom_qty": line.qty_done,
                                "location_id": picking.location_id.with_company(
                                    intercomp_picking.company_id.id
                                ).id,
                                "location_dest_id": (
                                    picking.location_dest_id.with_company(
                                        intercomp_picking.company_id.id
                                    ).id
                                ),
                                "move_orig_ids": [(4, line.move_id.id)],
                                "origin_returned_move_id": line.move_id.id,
                                "group_id": intercomp_picking.group_id.id,
                                "to_refund": True,
                                "company_id": intercomp_picking.company_id.id,
                                "move_line_ids": [
                                    (
                                        0,
                                        0,
                                        {
                                            "picking_id": picking.id,
                                            "product_id": line.product_id.id,
                                            "product_uom_id": line.product_uom_id.id,
                                            "qty_done": line.qty_done,
                                            "location_id": picking.location_id.with_company(
                                                intercomp_picking.company_id.id
                                            ).id,
                                            "location_dest_id": (
                                                picking.location_dest_id.with_company(
                                                    intercomp_picking.company_id.id
                                                ).id
                                            ),
                                            "company_id": intercomp_picking.company_id.id,
                                        },
                                    )
                                ],
                            }
                        )
                    )
                    line.move_id.write(
                        {
                            "move_dest_ids": [(4, move.id)],
                            "returned_move_ids": [(4, move.id)],
                        }
                    )
                picking.intercompany_picking_id = return_picking.id
                return_picking.intercompany_picking_id = picking.id
                picking.action_confirm()
        return new_picking, picking_type_id
