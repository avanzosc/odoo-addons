# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import unicodedata

from odoo import api, fields, models


def normalize_text(value):
    if not value:
        return ""

    return "".join(
        c
        for c in unicodedata.normalize("NFD", value)
        if unicodedata.category(c) != "Mn"
    ).lower()


class ResPartner(models.Model):
    _inherit = "res.partner"

    name_normalized = fields.Char(
        compute="_compute_normalized_fields",
        store=True,
    )
    city_normalized = fields.Char(
        compute="_compute_normalized_fields",
        store=True,
    )
    autonomous = fields.Boolean(string="He is self-employed?", default=False)

    @api.depends("name", "city")
    def _compute_normalized_fields(self):
        for partner in self:
            partner.name_normalized = normalize_text(partner.name)
            partner.city_normalized = normalize_text(partner.city)

    @api.depends_context("show_city")
    def _compute_display_name(self):
        result = super()._compute_display_name()
        if self.env.context.get("show_city"):
            for partner in self:
                display_name = ""
                if partner.city:
                    display_name = f"{partner.name} ({partner.city})"
                if partner.parent_id:
                    display_name = f"{partner.parent_id.name}, {display_name}"
                partner.display_name = display_name
        return result
