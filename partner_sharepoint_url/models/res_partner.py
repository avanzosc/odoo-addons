# Copyright (c) 2025 Aner Arregi <aneravanzosc@gmail.com> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    sharepoint_url = fields.Char(
        string="SharePoint URL",
        help="Link to SharePoint with technical information, drawings and documentation",
    )

    @api.constrains("sharepoint_url")
    def _check_sharepoint_url(self):
        for record in self:
            if record.sharepoint_url:
                if not record.sharepoint_url.startswith(("https://", "http://")):
                    raise ValidationError(_("URL must start with http:// or https://"))
