# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        related="serial_number_id.product_id",
        store=True,
        copy=False,
    )
    serial_number_id = fields.Many2one(
        string="Serial number", comodel_name="stock.production.lot", copy=False
    )
    type_id = fields.Many2one(
        string="Vehicle type", comodel_name="fleet.vehicle.model.type"
    )

    @api.onchange("model_id")
    def onchange_model_id(self):
        type_id = False
        if self.model_id and self.model_id.type_id:
            type_id = self.model_id.type_id.id
        self.type_id = type_id

    @api.model
    def create(self, values):
        vehicle = super().create(values)
        if "serial_number_id" in values and values.get("serial_number_id", False):
            serial_number = self.env["stock.production.lot"].browse(
                values.get("serial_number_id")
            )
            serial_number.with_context(no_update_vehicle=True).vehicle_id = vehicle.id
        return vehicle

    def write(self, vals):
        if (
            ("no_update_serial_number" not in self.env.context)
            and ("serial_number_id" in vals)
            and (vals.get("serial_number_id", False))
        ):
            for vehicle in self:
                if (
                    vehicle.serial_number_id
                    and vehicle.serial_number_id.id != vals.get("serial_number_id")
                ):
                    vehicle.serial_number_id.vehicle_id = False
        result = super().write(vals)
        if "no_update_serial_number" not in self.env.context and (
            "serial_number_id" in vals and vals.get("serial_number_id", False)
        ):
            serial_number = self.env["stock.production.lot"].browse(
                vals.get("serial_number_id")
            )
            serial_number.with_context(no_update_vehicle=True).vehicle_id = self.id
        return result
