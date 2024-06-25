# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    location_change_id = fields.Many2one(
        string="Location Change",
        comodel_name="stock.location",
        related="batch_id.location_change_id",
        store=True,
    )

    def button_validate(self):
        result = super().button_validate()
        for picking in self:
            if (
                picking.batch_id
                and (picking.batch_id.batch_type) == "mother"
                and not (picking.batch_id.start_laying_date)
            ):
                if picking.move_line_ids_without_package and any(
                    [
                        ml.product_id.egg
                        for ml in (picking.move_line_ids_without_package)
                    ]
                ):
                    picking.batch_id.start_laying_date = picking.custom_date_done.date()
        return result
