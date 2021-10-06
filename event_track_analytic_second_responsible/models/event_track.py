# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class EventTrack(models.Model):
    _inherit = 'event.track'

    def _create_analytic_line(self):
        result = super(EventTrack, self)._create_analytic_line()
        if self.second_responsible_id:
            values = self._catch_values_for_create_analytic_line(
                self.second_responsible_id)
            self.env['account.analytic.line'].create(values)
        return result
