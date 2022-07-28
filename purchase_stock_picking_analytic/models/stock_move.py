# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _prepare_data_for_create_analytic_line(self):
        self.ensure_one()
        if self.picking_id.purchase_id:
            return {}
        return super(StockMove, self)._prepare_data_for_create_analytic_line()
