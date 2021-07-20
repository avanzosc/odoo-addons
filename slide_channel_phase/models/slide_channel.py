# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    content_view = fields.Selection(
        [
            ("all", "Show whole course"),
            ("phase", "Show course on phase completion"),
        ],
        default="all",
        required=True,
        help="Choose how to show the course items on website",
    )
