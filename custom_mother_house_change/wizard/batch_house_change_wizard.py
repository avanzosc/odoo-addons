# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models, fields
from odoo.exceptions import ValidationError


class BatchHouseChangeWizard(models.TransientModel):
    _name = "batch.house.change.wizard"
    _description = "Wizard to change the house"

    def default_date_done(self):
        date = fields.Datetime.now()
        return date

    def _get_type_domain(self):
        batch = self.env["stock.picking.batch"].browse(
            self.env.context.get('active_id'))
        type = self.env.ref("stock_warehouse_farm.categ_type1")
        warehouses = self.env["stock.warehouse"].search(
            [("activity", "=", "reproduction"), ("type_id", "=", type.id)])
        location_dest = self.env["stock.location"].search(
            [("warehouse_id", "in", warehouses.ids)])
        domain = [("default_location_src_id", "=", batch.location_id.id),
                  ("default_location_dest_id", "in", location_dest.ids)]
        return domain

    type_id = fields.Many2one(
        string="Type",
        comodel_name="stock.picking.type",
        domain=_get_type_domain)
    date_done = fields.Datetime(
        string="Date Done",
        default=default_date_done)

    def button_change_house(self):
        batch = self.env["stock.picking.batch"].browse(
            self.env.context.get('active_id'))
        picking = batch.picking_ids.filtered(
                "custom_date_done")
        if not picking:
            raise ValidationError(
                _("No transfer found."))
        picking = min(
            picking, key=lambda x: x.custom_date_done)
        new_picking = self.env["stock.picking"].create({
            "batch_id": batch.id,
            "picking_type_id": self.type_id.id,
            "location_id": self.type_id.default_location_src_id.id,
            "location_dest_id": self.type_id.default_location_dest_id.id,
            "custom_date_done": self.date_done})
        for move in picking.move_ids_without_package:
            new_move = move.copy()
            new_move.write({
                "location_id": self.type_id.default_location_src_id.id,
                "location_dest_id": self.type_id.default_location_dest_id.id,
                "picking_id": picking.id})
            new_picking.move_ids_without_package = [(4, new_move.id)]
        new_picking.action_assign()
        new_picking.action_confirm()
        for line in new_picking.move_line_ids_without_package:
            if not line.qty_done:
                line.qty_done = line.product_uom_qty
        new_picking.button_validate()
        batch.write({
            "location_change_id": batch.location_id.id,
            "location_id": self.type_id.default_location_dest_id.id,
            "change_house_date": self.date_done.date(),
            "stage_id": (
                self.env.ref("stock_picking_batch_mother.batch_stage8").id)})
