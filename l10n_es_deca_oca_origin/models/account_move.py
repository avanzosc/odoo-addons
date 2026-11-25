from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    carrier_contact_id = fields.Many2one(
        comodel_name="res.partner",
        string="Carrier contact",
        help=(
            "Carrier contact whose name, VAT and address are printed on the DeCA. "
            "Use a shared contact or one belonging to the transfer company."
        ),
        check_company=True,
    )
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
    special_authorization = fields.Text(
        string="Special traffic authorisations",
        help=(
            "Traffic authorisations printed on the DeCA. Changes after completion "
            "retain previous values in the printed history."
        ),
    )
    deca_weight = fields.Float(
        digits=False,
        min_display_digits="Stock Weight",
        help=(
            "Total cargo weight in kg, excluding cancelled moves. Uses actual "
            "quantity when nonzero, otherwise planned quantity. Product weights "
            "are converted from the effective weight unit to kg. Up to six decimal "
            "places are shown; positive weights too small to display block issuance."
        ),
    )
    deca_notes = fields.Text(string="DECA Notes")
