# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    website_assorted_stains = fields.Char(
        string="Assorted Stains",
    )
    website_bottom_ply = fields.Char(
        string="Bottom Ply",
    )
    website_top_ply = fields.Char(
        string="Top Ply",
    )
    website_full_dip = fields.Char(
        string="Full Dip",
    )
    website_wheel_wells = fields.Char(
        string="Wheel Wells",
    )
    website_raised_ink = fields.Char(
        string="Raised Ink",
    )
    website_foil_ink = fields.Char(
        string="Foil Ink",
    )
    website_matte_finish = fields.Char(
        string="Matte Finish",
    )
