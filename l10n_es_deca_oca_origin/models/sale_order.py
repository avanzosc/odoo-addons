# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class SaleOrder(models.Model):
    _inherit = "sale.order"

    carrier_contact_id = fields.Many2one(
        comodel_name="res.partner",
        string="Carrier",
        help=(
            "Carrier contact whose name, VAT and address are printed on the DeCA. "
            "Use a shared contact or one belonging to the transfer company."
        ),
        check_company=True,
    )
    tractor_license_plate_id = fields.Many2one(
        string="Tractor licence plate",
        comodel_name="fleet.vehicle",
        help=(
            "Current licence plate printed on the DeCA. Changes after completion "
            "retain the previous value in the printed history."
        ),
    )
    trailer_license_plate_id = fields.Many2one(
        string="Trailer licence plate",
        comodel_name="fleet.vehicle",
        help=(
            "Current licence plate printed on the DeCA. Changes after completion "
            "retain the previous value in the printed history."
        ),
    )
    special_authorization = fields.Text(
        string="Special traffic authorisations",
        help=(
            "Traffic authorisations printed on the DeCA. Changes after completion "
            "retain previous values in the printed history."
        ),
    )
    deca_weight = fields.Float(
        compute="_compute_deca_weight",
        digits=False,
        min_display_digits="Stock Weight",
        store=True,
        help=(
            "Total cargo weight in kg, excluding cancelled moves. Uses actual "
            "quantity when nonzero, otherwise planned quantity. Product weights "
            "are converted from the effective weight unit to kg. Up to six decimal "
            "places are shown; positive weights too small to display block issuance."
        ),
        compute_sudo=True,
    )
    deca_notes = fields.Text(string="DECA Notes")
    sale_import_id = fields.Many2one(
        string="From Sale Import",
        comodel_name="sale.order.import",
        copy=False,
        readonly=True,
    )

    @api.onchange("tractor_license_plate_id")
    def _onchange_tractor_license_plate_id(self):
        self.carrier_contact_id = (
            self.tractor_license_plate_id.driver_id
            if self.tractor_license_plate_id
            else False
        )

    @api.depends("order_line", "order_line.deca_weight")
    def _compute_deca_weight(self):
        for sale in self:
            sale.deca_weight = sum(
                line.deca_weight for line in sale.order_line if line.deca_weight > 0
            )

    def action_confirm(self):
        self._check_deca_required_fields()
        return super().action_confirm()

    def _check_deca_required_fields(self):
        for sale in self:
            if any(
                weight > 0 and float_is_zero(weight, precision_digits=6)
                for weight in [
                    sale.deca_weight,
                    *sale.order_line.mapped("deca_weight"),
                ]
            ):
                raise UserError(
                    self.env._(
                        "A positive DeCA weight is too small to display in kg with six "
                        "decimal places. Review the cargo before generating "
                        "the document."
                    )
                )
            missing = []
            if not sale.tractor_license_plate_id:
                missing.append(
                    self.env._(
                        "You must define the Main vehicle or tractor licence plate."
                    )
                )
            if not sale.carrier_contact_id:
                missing.append(self.env._("You must define the Carrier contact."))
            elif not sale.carrier_contact_id.vat:
                missing.append(self.env._("Carrier NIF (VAT)"))
            for line in sale.order_line.filtered(lambda x: not x.display_type):
                product_data = {
                    "product_name": line.product_id.name,
                    "quantity": line.product_uom_qty,
                    "deca_weight": line.deca_weight,
                }
                if not line.place_of_loading_id:
                    missing.append(
                        self.env._(
                            "You must define the Place of loading"
                            " for product: %(product_name)s, quantity: "
                            "%(quantity)s, DECA Weight: %(deca_weight)s"
                        )
                        % product_data
                    )
                elif not line.place_of_loading_id.vat:
                    missing.append(
                        self.env._(
                            "You must define the VAT for Sender / Place"
                            " of loading: %(sender_name)s for product:"
                            " %(product_name)s, quantity: %(quantity)s,"
                            " DECA Weight: %(deca_weight)s"
                        )
                        % {
                            **product_data,
                            "sender_name": line.place_of_loading_id.name,
                        }
                    )
                if not line.place_of_delivery_id:
                    missing.append(
                        self.env._(
                            "You must define the Place of delivery"
                            " for product: %(product_name)s, quantity:"
                            " %(quantity)s, DECA Weight: %(deca_weight)s"
                        )
                        % product_data
                    )
                elif not line.place_of_delivery_id.vat:
                    missing.append(
                        self.env._(
                            "You must define the VAT for Consignee / Place"
                            " of delivery: %(consignee_name)s for product:"
                            " %(product_name)s, quantity: %(quantity)s,"
                            " DECA Weight: %(deca_weight)s"
                        )
                        % {
                            **product_data,
                            "consignee_name": line.place_of_delivery_id.name,
                        }
                    )
            if not sale.deca_weight:
                missing.append(self.env._("Weight"))
            if missing:
                raise UserError(
                    self.env._(
                        "The following data is missing for the DeCA"
                        " report for sale %(sale)s:\n%(missing)s",
                        sale=sale.name,
                        missing="\n".join([f"- {m}" for m in missing]),
                    )
                )
