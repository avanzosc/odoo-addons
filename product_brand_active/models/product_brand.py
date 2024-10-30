# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProductBrand(models.Model):
    _inherit = "product.brand"

    active = fields.Boolean(default=True, copy=False)
    start_date = fields.Date(copy=False)
    end_date = fields.Date(copy=False)

    @api.onchange("active")
    def onchange_active(self):
        self.end_date = False if self.active else fields.Date.context_today(self)
