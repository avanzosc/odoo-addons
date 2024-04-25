# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    file_number = fields.Char(
        string=_("File Number"),
        copy=False,
    )
    building_use_id = fields.Many2one("building.use", string=_("Building Use"))
    certification_text = fields.Text(string=_("Certification Text"))
    emi = fields.Text(string=_("Emi"))
    epi = fields.Text(string=_("Epi"))

    title = fields.Char(
        string=_("Title"),
        domain="[('is_company','=',False)]",
        help=_("Title of the individual contact."),
    )
    membership_number = fields.Char(
        string=_("Membership Number"),
        domain="[('is_company','=',False)]",
        help=_("Membership number of the individual contact."),
    )
