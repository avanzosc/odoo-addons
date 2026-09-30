# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    barcode_prefix = fields.Integer(
        help="Used to auto-generate product barcodes (EAN13). 7 digits maximum.",
    )

    @api.constrains("barcode_prefix")
    def _check_barcode_prefix(self):
        for company in self:
            if company.barcode_prefix > 9999999:
                raise ValidationError(
                    _("The barcode prefix must have 7 digits maximum.")
                )
