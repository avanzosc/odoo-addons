# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        result = super().button_validate()
        for picking in self:
            if (
                picking.batch_id
                and picking.batch_id.batch_type == "mother"
                and not picking.batch_id.start_laying_date
                and picking.custom_date_done
                and any(
                    ml.product_id.product_tmpl_id.egg
                    for ml in picking.move_line_ids_without_package
                )
            ):
                picking.batch_id.start_laying_date = fields.Date.to_date(
                    picking.custom_date_done
                )
        return result
