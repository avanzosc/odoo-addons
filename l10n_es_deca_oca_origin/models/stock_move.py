# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    place_of_loading_id = fields.Many2one(
        string="Place of loading", comodel_name="res.partner"
    )
    char_place_loading = fields.Char(
        string="Place of loading", compute="_compute_char_place_loading"
    )
    place_of_delivery_id = fields.Many2one(
        string="Place of delivery", comodel_name="res.partner"
    )
    char_place_delivery = fields.Char(
        string="Place of delivery", compute="_compute_char_place_delivery"
    )
    upload_date = fields.Date(
        copy=False,
    )
    deca_weight = fields.Float(readonly=False, compute=False, compute_sudo=False)

    carrier_contact_id = fields.Many2one(
        comodel_name="res.partner",
        string="Carrier",
        help=(
            "Carrier contact whose name, VAT and address are printed on the DeCA. "
            "Use a shared contact or one belonging to the transfer company."
        ),
        check_company=True,
        related="picking_id.carrier_contact_id",
        store=True,
    )
    tractor_license_plate_id = fields.Many2one(
        string="Tractor licence plate",
        comodel_name="fleet.vehicle",
        help=(
            "Current licence plate printed on the DeCA. Changes after completion "
            "retain the previous value in the printed history."
        ),
        related="picking_id.tractor_license_plate_id",
        store=True,
    )
    trailer_license_plate_id = fields.Many2one(
        string="Trailer licence plate",
        comodel_name="fleet.vehicle",
        help=(
            "Current licence plate printed on the DeCA. Changes after completion "
            "retain the previous value in the printed history."
        ),
        related="picking_id.trailer_license_plate_id",
        store=True,
    )
    special_authorization = fields.Text(
        string="Special traffic authorisations",
        help=(
            "Traffic authorisations printed on the DeCA. Changes after completion "
            "retain previous values in the printed history."
        ),
        related="picking_id.special_authorization",
        store=True,
    )

    def _compute_char_place_loading(self):
        for move in self:
            move.char_place_loading = move._partner_data_in_char_type(
                move.place_of_loading_id
            )

    def _compute_char_place_delivery(self):
        for move in self:
            move.char_place_delivery = move._partner_data_in_char_type(
                move.place_of_delivery_id
            )

    def _get_new_picking_values(self):
        vals = super()._get_new_picking_values()
        vals["carrier_contact_id"] = self.sale_line_id.order_id.carrier_contact_id.id
        vals["deca_weight"] = self.sale_line_id.order_id.deca_weight
        vals["deca_notes"] = self.sale_line_id.order_id.deca_notes
        if self.sale_line_id.order_id.tractor_license_plate_id:
            vals["tractor_license_plate_id"] = (
                self.sale_line_id.order_id.tractor_license_plate_id.id
            )
        if self.sale_line_id.order_id.trailer_license_plate_id:
            vals["trailer_license_plate_id"] = (
                self.sale_line_id.order_id.trailer_license_plate_id.id
            )
        if self.sale_line_id.order_id.special_authorization:
            vals["special_authorization"] = (
                self.sale_line_id.order_id.special_authorization
            )
        return vals

    @api.model
    def _partner_data_in_char_type(self, partner):
        if not partner or not partner.contact_address:
            return ""
        lines = [
            line.strip()
            for line in partner.contact_address.splitlines()
            if line.strip()
        ]
        if lines and partner.country_id and partner.country_id.code == "ES":
            lines = lines[:-1]
        return ", ".join(lines)
