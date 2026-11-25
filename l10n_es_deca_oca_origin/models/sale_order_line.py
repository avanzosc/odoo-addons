# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    place_of_loading_id = fields.Many2one(
        string="Place of loading", comodel_name="res.partner"
    )
    place_of_delivery_ids = fields.Many2many(
        string="Place of delivery", comodel_name="res.partner"
    )
    upload_date = fields.Date(
        copy=False,
    )
    occupation = fields.Float(
        copy=False,
    )
    deca_weight = fields.Float(
        digits=False,
        min_display_digits="Stock Weight",
        help=(
            "Weight in kg, excluding cancelled moves. Up to six decimal "
            "places are shown; positive weights too small to display block issuance."
        ),
        default=0,
    )
    carrier_contact_id = fields.Many2one(
        comodel_name="res.partner",
        string="Carrier",
        help=(
            "Carrier contact whose name, VAT and address are printed on the DeCA. "
            "Use a shared contact or one belonging to the transfer company."
        ),
        check_company=True,
        related="order_id.carrier_contact_id",
        store=True,
    )
    tractor_license_plate_id = fields.Many2one(
        string="Tractor licence plate",
        comodel_name="fleet.vehicle",
        help=(
            "Current licence plate printed on the DeCA. Changes after completion "
            "retain the previous value in the printed history."
        ),
        related="order_id.tractor_license_plate_id",
        store=True,
    )
    trailer_license_plate_id = fields.Many2one(
        string="Trailer licence plate",
        comodel_name="fleet.vehicle",
        help=(
            "Current licence plate printed on the DeCA. Changes after completion "
            "retain the previous value in the printed history."
        ),
        related="order_id.trailer_license_plate_id",
        store=True,
    )
    special_authorization = fields.Text(
        string="Special traffic authorisations",
        help=(
            "Traffic authorisations printed on the DeCA. Changes after completion "
            "retain previous values in the printed history."
        ),
        related="order_id.special_authorization",
        store=True,
    )

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        values = super()._prepare_invoice_line(**optional_values)
        values.update(
            {
                "place_of_loading_id": self.place_of_loading_id.id,
                "place_of_delivery_ids": [(6, 0, self.place_of_delivery_ids.ids)],
                "upload_date": self.upload_date,
                "occupation": self.occupation,
                "deca_weight": self.deca_weight,
                "carrier_contact_id": self.carrier_contact_id.id,
                "tractor_license_plate_id": self.tractor_license_plate_id.id,
                "trailer_license_plate_id": self.trailer_license_plate_id.id,
                "special_authorization": self.special_authorization,
            }
        )
        return values
