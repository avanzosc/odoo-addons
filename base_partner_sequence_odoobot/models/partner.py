# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _needs_ref(self, vals=None):
        if self.customer_from_woo:
            return True
        return super()._needs_ref(vals)
