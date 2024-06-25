# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    custom_date_done = fields.Datetime(string="Date Realized")

    def button_validate(self):
        if any(self.filtered(lambda p: not p.custom_date_done)):
            raise ValidationError(_("You must introduce the date realized"))
        return super().button_validate()

    def write(self, vals):
        result = super().write(vals)
        if "custom_date_done" in vals:
            for line in self:
                for move in line.move_ids_without_package:
                    move.date = line.custom_date_done
                for move_line in line.move_line_ids_without_package:
                    move_line.date = line.custom_date_done
        return result
