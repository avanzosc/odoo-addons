# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"
    _order = "custom_date_done desc, priority desc, scheduled_date asc, id desc"

    def button_validate(self):
        for picking in self:
            if not picking.crm_driver_id:
                picking.crm_driver_id = self.env.user.partner_id.id
        return super().button_validate()
