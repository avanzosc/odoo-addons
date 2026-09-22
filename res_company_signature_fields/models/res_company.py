# Copyright 2025 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    signature_image = fields.Image(copy=False)
    stamp_image = fields.Image(copy=False)
