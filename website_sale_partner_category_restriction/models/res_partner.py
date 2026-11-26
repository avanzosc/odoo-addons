# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_restriction_categories(self):
        partner = self.sudo()
        return partner.category_id | partner.commercial_partner_id.category_id
