# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def do_cancel_done(self):
        for picking in self:
            picking.move_ids_without_package.do_cancel_done()
