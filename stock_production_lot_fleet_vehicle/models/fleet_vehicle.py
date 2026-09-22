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
        string="Serial number", comodel_name="stock.lot", copy=False
    )
    type_id = fields.Many2one(
        string="Vehicle type", comodel_name="fleet.vehicle.model.type"
    )

    @api.onchange("model_id")
    def onchange_model_id(self):
        self.type_id = self.model_id.type_id.id if self.model_id.type_id else False

    @staticmethod
    def _to_m2o_value(value):
        if isinstance(value, int):
            return value
        if hasattr(value, "id"):
            return value.id
        if isinstance(value, list | tuple) and value:
            command = value[0]
            if command in (4, 6):
                ids = value[1] if command == 4 else value[2]
                if isinstance(ids, list):
                    return ids[0] if ids else False
                return ids
        return False

    @classmethod
    def _extract_serial_number_id(cls, vals):
        return cls._to_m2o_value(vals.get("serial_number_id"))

    @classmethod
    def _is_sync_enabled(cls, env):
        return "no_update_serial_number" not in env.context

    def create(self, vals_list):
        vehicles = super().create(vals_list)
        if not self._is_sync_enabled(self.env):
            return vehicles

        if isinstance(vals_list, dict):
            vals_list = [vals_list]
            vehicles = vehicles if len(vehicles) > 1 else vehicles

        for vehicle, vals in zip(vehicles, vals_list, strict=False):
            serial_number_id = self._extract_serial_number_id(vals)
            if serial_number_id:
                self.env["stock.lot"].browse(serial_number_id).with_context(
                    no_update_vehicle=True
                ).vehicle_id = vehicle.id
        return vehicles

    def write(self, vals):
        if "serial_number_id" in vals and self._is_sync_enabled(self.env):
            new_serial_number_id = self._extract_serial_number_id(vals)
            if new_serial_number_id:
                for vehicle in self:
                    if vehicle.serial_number_id.id != new_serial_number_id:
                        vehicle.serial_number_id.with_context(
                            no_update_vehicle=True
                        ).vehicle_id = False
            else:
                for vehicle in self.filtered("serial_number_id"):
                    vehicle.serial_number_id.with_context(
                        no_update_vehicle=True
                    ).vehicle_id = False

        result = super().write(vals)

        if "serial_number_id" in vals and self._is_sync_enabled(self.env):
            for vehicle in self.filtered("serial_number_id"):
                vehicle.serial_number_id.with_context(
                    no_update_vehicle=True
                ).vehicle_id = vehicle.id
        return result
