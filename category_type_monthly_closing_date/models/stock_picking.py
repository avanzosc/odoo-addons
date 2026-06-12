# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:
            local_date = (
                fields.Datetime.context_timestamp(
                    picking, picking.custom_date_done
                ).date()
                if picking.custom_date_done
                else None
            )
            if (
                local_date
                and picking.category_type_id
                and picking.category_type_id.monthly_closing_date
                and local_date <= picking.category_type_id.monthly_closing_date
            ):
                raise ValidationError(
                    _(
                        "The date of the picking cannot be earlier "
                        + "than the monthly closing date of the sections."
                    )
                )
            if (
                local_date
                and picking.dest_category_type_id
                and picking.dest_category_type_id.monthly_closing_date
                and local_date <= picking.dest_category_type_id.monthly_closing_date
            ):
                raise ValidationError(
                    _(
                        "The date of the picking cannot be earlier "
                        + "than the monthly closing date of the sections."
                    )
                )
        return super().button_validate()
