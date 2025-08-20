# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    sale_fiscal_position_id = fields.Many2one(
        comodel_name="account.fiscal.position",
        string="Fiscal position for sales",
    )
