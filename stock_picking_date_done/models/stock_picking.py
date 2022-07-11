# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    custom_date_done = fields.Datetime(string='Date realized')

    def button_validate(self):
        result = super(StockPicking, self).button_validate()
        if not self.custom_date_done:
            raise ValidationError(
                _("You must introduce the done date."))
        return result
