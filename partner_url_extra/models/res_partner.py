# Copyright (c) 2025 AvanzOSC S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    extra_url = fields.Char(
        string="Extra URL",
        help="Extra URL for technical information, drawings, documentation or any other link",
    )

    @api.constrains("extra_url")
    def _check_extra_url(self):
        """Validate URL format"""
        for record in self:
            if record.extra_url:
                if not record.extra_url.startswith(("https://", "http://")):
                    raise ValidationError(_("URL must start with http:// or https://"))
