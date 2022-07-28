# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.depends("picking_type_id", "picking_type_id.code")
    def _compute_show_analytic_account(self):
        super(StockPicking, self)._compute_show_analytic_account()
        for record in self.filtered("purchase_id"):
            record.show_analytic_account = False
