# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    copy_main_responsible = fields.Boolean(
        string='Copy main responsible', default=False)
    copy_second_responsible = fields.Boolean(
        string='Copy second responsible', default=False)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if not self.copy_main_responsible:
            default['main_responsible_id'] = False
        if not self.copy_second_responsible:
            default['second_responsible_id'] = False
        return super(EventEvent, self).copy(default)
