# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SacaLine(models.Model):
    _inherit = "saca.line"

    def _get_quality_responsible(self):
        responsible = self.env["res.partner"]
        responsible_categ = self.env.ref("custom_saca.quality_responsible_category")
        if responsible_categ:
            responsible = self.env["res.partner"].search([("category_id", "=", responsible_categ.id)])
        return responsible
