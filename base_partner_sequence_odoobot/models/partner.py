# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _needs_ref(self, vals=None):
        res super()._needs_ref(vals)
        return self.create_uid == 1 and res
