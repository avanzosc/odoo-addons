# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class BatchHouseChangeWizard(models.TransientModel):
    _name = "batch.house.change.wizard"
    _description = "Wizard to change the house"

    def _get_valid_type_ids(self):
        batch = self.env["stock.picking.batch"].browse(
            self.env.context.get("active_id")
        )
        categ_type = self.env.ref("stock_warehouse_farm.categ_type1")
        warehouses = self.env["stock.warehouse"].search(
            [("activity", "=", "reproduction"), ("type_id", "=", categ_type.id)]
        )
        location_dest = self.env["stock.location"].search(
            [("warehouse_id", "in", warehouses.ids)]
        )
        return self.env["stock.picking.type"].search(
            [
                ("default_location_src_id", "=", batch.location_id.id),
                ("default_location_dest_id", "in", location_dest.ids),
            ]
        )

    valid_type_ids = fields.Many2many(
        comodel_name="stock.picking.type",
        default=_get_valid_type_ids,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="stock.picking.type",
        domain="[('id', 'in', valid_type_ids)]",
    )
    date_done = fields.Datetime(default=fields.Datetime.now)

    def button_change_house(self):
        if not self.type_id:
            raise ValidationError(_("You must select an operation type."))
        batch = self.env["stock.picking.batch"].browse(
            self.env.context.get("active_id")
        )
        pickings = batch.picking_ids.filtered(
            lambda c: c.state == "done" and c.picking_type_code == "incoming"
        )
        if not pickings:
            raise ValidationError(_("No transfer found."))
        for picking in pickings:
            new_picking = self.env["stock.picking"].create(
                {
                    "batch_id": batch.id,
                    "picking_type_id": self.type_id.id,
                    "location_id": self.type_id.default_location_src_id.id,
                    "location_dest_id": self.type_id.default_location_dest_id.id,
                    "custom_date_done": self.date_done,
                }
            )
            for move in picking.move_ids_without_package:
                self.env["stock.move"].create(
                    {
                        "name": move.name,
                        "product_id": move.product_id.id,
                        "product_uom": move.product_uom.id,
                        "product_uom_qty": move.product_uom_qty,
                        "location_id": self.type_id.default_location_src_id.id,
                        "location_dest_id": self.type_id.default_location_dest_id.id,
                        "picking_id": new_picking.id,
                        "picking_type_id": self.type_id.id,
                    }
                )
            new_picking.action_confirm()
            new_picking.button_force_done_detailed_operations()
            for line in new_picking.move_line_ids_without_package:
                if not line.quantity:
                    line.quantity = line.move_id.product_uom_qty
                line.picked = True
            new_picking.button_validate()
        batch.write(
            {
                "location_change_id": batch.location_id.id,
                "location_id": self.type_id.default_location_dest_id.id,
                "change_house_date": self.date_done.date(),
                "stage_id": (
                    self.env.ref("stock_picking_batch_mother.batch_stage8").id
                ),
            }
        )
