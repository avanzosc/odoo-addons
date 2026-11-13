# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.exceptions import UserError


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
                picking.tractor_license_plate = (
                    picking.tractor_license_plate_id.license_plate
                )

            if picking.trailer_license_plate_id:
                picking.trailer_license_plate = (
                    picking.trailer_license_plate_id.license_plate
                )
            else:
                picking.trailer_license_plate = ""
            if not picking.carrier_contact_id:
                missing.append(self.env._("You must define the Carrier contact."))
            elif not picking.carrier_contact_id.vat:
                missing.append(self.env._("Carrier NIF (VAT)"))
            for move in picking.move_ids_without_package.filtered(
                lambda x: x.product_id
            ):
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
                if not move.place_of_delivery_id:
                    missing.append(
                        self.env._(
                            "You must define the Place of delivery"
                            " for product: %(product_name)s, quantity: "
                            "%(quantity)s, DECA Weight: %(deca_weight)s"
                        )
                        % product_data
                    )
                elif not move.place_of_delivery_id.vat:
                    missing.append(
                        self.env._(
                            "You must define the VAT for Consignee / Place"
                            " of delivery: %(consignee_name)s for product:"
                            " %(product_name)s, quantity: %(quantity)s, "
                            "DECA Weight: %(deca_weight)s"
                        )
                        % {
                            **product_data,
                            "consignee_name": move.place_of_delivery_id.name,
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

    def _get_deca_report_data(self):
        self.ensure_one()
        values = super()._get_deca_report_data()
        contractual = {
            name: self.partner_id[name] or ""
            for name in ("name", "vat", "street", "zip", "city")
        } | {
            "state": self.partner_id.state_id.name or "",
            "country": self.partner_id.country_id.name or "",
        }

        contractual = {
            name: self.partner_id[name] or ""
            for name in ("name", "vat", "street", "zip", "city")
        } | {
            "state": self.partner_id.state_id.name or "",
            "country": self.partner_id.country_id.name or "",
        }
        values.update(
            {
                "contractual": contractual,
                "tractor_license_plate": self.tractor_license_plate_id.license_plate,
                "deca_notes": self.deca_notes,
            }
        )
        if self.trailer_license_plate_id:
            values.update(
                {
                    "trailer_license_plate": (
                        self.trailer_license_plate_id.license_plate
                    ),
                }
            )
        for goods, move in zip(values["goods"], self.move_ids, strict=False):
            goods["upload_date"] = (
                move.upload_date.strftime("%d/%m/%Y") if move.upload_date else ""
            )
            goods["place_of_loading"] = move._partner_data_in_char_type(
                move.place_of_loading_id
            )
            goods["place_of_delivery"] = move._partner_data_in_char_type(
                move.place_of_delivery_id
            )
        return values
