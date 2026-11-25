# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import hashlib
import re

from odoo import api, fields, models
from odoo.exceptions import UserError

# Separators allowed in fleet plates but not stored on the DeCA (max. 8 chars).
PLATE_SEPARATORS_RE = re.compile(r"[\s.\-]")


class StockPicking(models.Model):
    _inherit = "stock.picking"

    tractor_license_plate_id = fields.Many2one(
        string="Main vehicle or tractor licence plate",
        comodel_name="fleet.vehicle",
        help=(
            "Current licence plate printed on the DeCA. Changes after completion "
            "retain the previous value in the printed history."
        ),
    )
    trailer_license_plate_id = fields.Many2one(
        string="Trailer or semi-trailer licence plate",
        comodel_name="fleet.vehicle",
        help=(
            "Current licence plate printed on the DeCA. Changes after completion "
            "retain the previous value in the printed history."
        ),
    )
    deca_notes = fields.Text(string="DECA Notes")

    # Vehicle field -> DeCA char field of l10n_es_deca_oca whose changes are
    # kept in the history printed (struck through) on the DeCA.
    _DECA_VEHICLE_PLATE_FIELDS = {
        "tractor_license_plate_id": "tractor_license_plate",
        "trailer_license_plate_id": "trailer_license_plate",
    }

    def _prepare_deca_plate_vals(self, vals):
        """Add to ``vals`` the normalized plate of the vehicles being written,
        so the base ``write`` stores the previous plate in the DeCA history.
        Plates longer than the field size are left for
        ``_check_deca_required_fields``, which reports them."""
        vals = dict(vals)
        for vehicle_field, plate_field in self._DECA_VEHICLE_PLATE_FIELDS.items():
            if vehicle_field not in vals or plate_field in vals:
                continue
            vehicle = self.env["fleet.vehicle"].browse(vals[vehicle_field])
            plate = self._get_deca_license_plate(vehicle) if vehicle else ""
            size = self._fields[plate_field].size
            if not size or len(plate) <= size:
                vals[plate_field] = plate
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [self._prepare_deca_plate_vals(vals) for vals in vals_list]
        return super().create(vals_list)

    def write(self, vals):
        return super().write(self._prepare_deca_plate_vals(vals))

    def _get_deca_hash(self):
        """Also detect a change of vehicle, even if it has the same plate."""
        self.ensure_one()
        data = super()._get_deca_hash()
        data += f"{self.tractor_license_plate_id.id}{self.trailer_license_plate_id.id}"
        return hashlib.md5(data.encode("utf-8")).hexdigest()

    def _get_deca_license_plate(self, vehicle):
        """Return the vehicle plate as printed on the DeCA: without spaces,
        dots or hyphens and in upper case (e.g. R-8297-BCS -> R8297BCS)."""
        return PLATE_SEPARATORS_RE.sub("", vehicle.license_plate or "").upper()

    def _set_deca_license_plate(self, field_name, vehicle, missing):
        """Copy the normalized plate into the DeCA field, which only allows
        ``size`` characters; report it as missing data instead of failing."""
        plate = self._get_deca_license_plate(vehicle)
        size = self._fields[field_name].size
        if size and len(plate) > size:
            missing.append(
                self.env._(
                    "The licence plate %(plate)s of vehicle %(vehicle)s is longer "
                    "than %(size)s characters.",
                    plate=vehicle.license_plate,
                    vehicle=vehicle.display_name,
                    size=size,
                )
            )
        elif self[field_name] != plate:
            self[field_name] = plate

    def _check_deca_required_fields(self):
        for picking in self:
            missing = []
            if not picking.tractor_license_plate_id:
                missing.append(
                    self.env._(
                        "You must define the Main vehicle or tractor licence plate."
                    )
                )
            else:
                picking._set_deca_license_plate(
                    "tractor_license_plate", picking.tractor_license_plate_id, missing
                )

            if picking.trailer_license_plate_id:
                picking._set_deca_license_plate(
                    "trailer_license_plate", picking.trailer_license_plate_id, missing
                )
            elif picking.trailer_license_plate:
                picking.trailer_license_plate = ""
            if not picking.carrier_contact_id:
                missing.append(self.env._("You must define the Carrier contact."))
            elif not picking.carrier_contact_id.vat:
                missing.append(self.env._("Carrier NIF (VAT)"))
            for move in picking.move_ids.filtered(lambda x: x.product_id):
                product_data = {
                    "product_name": move.product_id.name,
                    "quantity": move.product_uom_qty,
                    "deca_weight": move.deca_weight,
                }
                if not move.place_of_loading_id:
                    missing.append(
                        self.env._(
                            "You must define the Place of loading"
                            " for product: %(product_name)s, quantity: "
                            "%(quantity)s, DECA Weight: %(deca_weight)s"
                        )
                        % product_data
                    )
                elif not move.place_of_loading_id.vat:
                    missing.append(
                        self.env._(
                            "You must define the VAT for Sender / Place"
                            " of loading: %(sender_name)s for product: "
                            "%(product_name)s, quantity: %(quantity)s,"
                            " DECA Weight: %(deca_weight)s"
                        )
                        % {
                            **product_data,
                            "sender_name": move.place_of_loading_id.name,
                        }
                    )
                if not move.place_of_delivery_ids:
                    missing.append(
                        self.env._(
                            "You must define the Place of delivery"
                            " for product: %(product_name)s, quantity:"
                            " %(quantity)s, DECA Weight: %(deca_weight)s"
                        )
                        % product_data
                    )
                else:
                    for delivery in move.place_of_delivery_ids:
                        if not delivery.vat:
                            missing.append(
                                self.env._(
                                    "You must define the VAT for Consignee / Place"
                                    " of delivery: %(consignee_name)s for product:"
                                    " %(product_name)s, quantity: %(quantity)s,"
                                    " DECA Weight: %(deca_weight)s"
                                )
                                % {
                                    **product_data,
                                    "consignee_name": delivery.name,
                                }
                            )
            if missing:
                raise UserError(
                    self.env._(
                        "The following data is missing for the DeCA "
                        "report for picking %(picking)s:\n%(missing)s",
                        picking=picking.name,
                        missing="\n".join(f"- {m}" for m in missing),
                    )
                )
        return super()._check_deca_required_fields()
