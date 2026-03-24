# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from dateutil.relativedelta import relativedelta

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        result = super()._action_done()
        for picking in self.filtered(
            lambda x: x.state == "done" and x.picking_type_id.code == "outgoing"
        ):
            lines = picking._find_lines_to_put_in_lot_expiration_date()
            for line in lines:
                line.lot_id.expiration_date = fields.Datetime.now() + relativedelta(
                    days=line.product_id.expiration_time
                )
        return result

    def _find_lines_to_put_in_lot_expiration_date(self):
        lines = self.move_line_ids_without_package.filtered(lambda x: x.lot_id)
        return lines
