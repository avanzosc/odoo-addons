# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def action_view_attachment(self):
        self.ensure_one()
        url = "/web/content/%s" % self.id
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }
