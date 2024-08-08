# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    search_phone = fields.Char(compute="_compute_search_phone", store=True, copy=False)
    search_mobile = fields.Char(
        compute="_compute_search_mobile", store=True, copy=False
    )

    @api.depends("phone")
    def _compute_search_phone(self):
        for partner in self:
            search_phone = ""
            if partner.phone:
                search_phone = partner.phone.replace(" ", "")
            partner.search_phone = search_phone

    @api.depends("mobile")
    def _compute_search_mobile(self):
        for partner in self:
            search_mobile = ""
            if partner.mobile:
                search_mobile = partner.mobile.replace(" ", "")
            partner.search_mobile = search_mobile
