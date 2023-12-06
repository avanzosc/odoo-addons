# Copyright 2023 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCityZip(models.Model):
    _inherit = "res.city.zip"

    state_id = fields.Many2one(
        related="city_id.state_id",
        comodel_name="res.country.state",
        string="State",
        store=True,
        copy=False,
    )
    country_id = fields.Many2one(
        related="city_id.country_id",
        comodel_name="res.country",
        string="Country",
        store=True,
        copy=False,
    )
