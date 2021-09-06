# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    name = fields.Char(default="/")

    @api.model
    def create(self, values):
        event = super(EventEvent, self).create(values)
        name = ''
        if event.lang_id and event.lang_id.code:
            name = event.lang_id.code
        if event.date_begin:
            name = (event.date_begin.year if not name else
                    '{}-{}'.format(name, event.date_begin.year))
        name = event.id if not name else '{}-{}'.format(name, event.id)
        event.name = name
        return event

    def write(self, values):
        if (('lang_id' in values and values.get('lang_id', False)) or
                ('date_begin' in values and values.get('date_begin', False))):
            name = ''
            if 'lang_id' in values and values.get('lang_id', False):
                lang = self.env['hr.skill'].browse(values.get('lang_id'))
                name = lang.code
            else:
                name = self.lang_id.code
            if 'date_begin' in values and values.get('date_begin', False):
                date_begin = fields.Datetime.from_string(
                    values.get('date_begin'))
                name = (date_begin.year if not name else
                        '{}-{}'.format(name, date_begin.year))
            else:
                name = self.date_begin.year()
            name = self.id if not name else '{}-{}'.format(name, self.id)
            values['name'] = name
        result = super(EventEvent, self).write(values)
        return result
