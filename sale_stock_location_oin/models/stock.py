# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class StockLocation(models.Model):
    _inherit = 'stock.location'

    eligible_for_sales = fields.Boolean(
        string='Eligible for sales', default=False)
