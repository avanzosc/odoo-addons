from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

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
        store=True,
    )
    tractor_license_plate_id = fields.Many2one(
        string="Tractor licence plate",
        comodel_name="fleet.vehicle",
        help=(
            "Current licence plate printed on the DeCA. Changes after completion "
            "retain the previous value in the printed history."
        ),
        store=True,
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
