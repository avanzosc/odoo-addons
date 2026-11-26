# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.lot"

    vehicle_id = fields.Many2one(string="Vehicle", comodel_name="fleet.vehicle")

    @staticmethod
    def _get_vehicle_id_from_vals(vals):
        """Normalize Many2one value from write/create vals."""
        vehicle = vals.get("vehicle_id")
        if hasattr(vehicle, "id"):
            return vehicle.id
        return vehicle

    @staticmethod
    def _to_m2o_value(value):
        """Support both int and command tuple/list values."""
        if isinstance(value, int):
            return value
        if isinstance(value, list | tuple) and value:
            command = value[0]
            if command in (4, 6):
                ids = value[1] if command == 4 else value[2]
                if isinstance(ids, list):
                    return ids[0] if ids else False
                return ids
            if command == 0 and len(value) > 2 and isinstance(value[2], dict):
                return value[2].get("id")
        return False

    @classmethod
    def _extract_vehicle_id(cls, vals):
        return cls._to_m2o_value(cls._get_vehicle_id_from_vals(vals))

    @classmethod
    def _has_field_in_vals(cls, vals):
        return "vehicle_id" in vals

    @classmethod
    def _is_sync_enabled(cls, env):
        return "no_update_vehicle" not in env.context

    @classmethod
    def _sync_lot_to_vehicle(cls, lot, vehicle_id):
        if vehicle_id:
            lot.env["fleet.vehicle"].browse(vehicle_id).with_context(
                no_update_serial_number=True
            ).serial_number_id = lot.id

    @classmethod
    def _clear_previous_vehicle_links(cls, lots, new_vehicle_id):
        for lot in lots:
            if lot.vehicle_id and lot.vehicle_id.id != new_vehicle_id:
                lot.vehicle_id.with_context(
                    no_update_serial_number=True
                ).serial_number_id = False

    @classmethod
    def _clear_vehicle_link_if_removed(cls, lots):
        for lot in lots.filtered("vehicle_id"):
            lot.vehicle_id.with_context(
                no_update_serial_number=True
            ).serial_number_id = False

    @classmethod
    def _sync_create(cls, lot, vals):
        vehicle_id = cls._extract_vehicle_id(vals)
        cls._sync_lot_to_vehicle(lot, vehicle_id)

    @classmethod
    def _sync_write(cls, lots, vals):
        if not cls._has_field_in_vals(vals) or not cls._is_sync_enabled(lots.env):
            return

        new_vehicle_id = cls._extract_vehicle_id(vals)
        if new_vehicle_id:
            cls._clear_previous_vehicle_links(lots, new_vehicle_id)
        else:
            cls._clear_vehicle_link_if_removed(lots)

    @classmethod
    def _sync_after_write(cls, lots, vals):
        if not cls._has_field_in_vals(vals) or not cls._is_sync_enabled(lots.env):
            return

        new_vehicle_id = cls._extract_vehicle_id(vals)
        if new_vehicle_id:
            lots_with_vehicle = lots.filtered(
                lambda lot: lot.vehicle_id.id == new_vehicle_id
            )
            for lot in lots_with_vehicle:
                cls._sync_lot_to_vehicle(lot, new_vehicle_id)

    @classmethod
    def _sync_create_post(cls, lot, vals):
        if cls._is_sync_enabled(lot.env):
            cls._sync_create(lot, vals)

    def create(self, vals_list):
        lots = super().create(vals_list)
        if isinstance(vals_list, dict):
            self._sync_create_post(lots, vals_list)
            return lots

        for lot, vals in zip(lots, vals_list, strict=False):
            self._sync_create_post(lot, vals)
        return lots

    def write(self, vals):
        self._sync_write(self, vals)
        result = super().write(vals)
        self._sync_after_write(self, vals)
        return result
