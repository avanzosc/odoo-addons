# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _get_user_lang(self):
        return self.env.lang