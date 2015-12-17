# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class Schedule(models.Model):
    _name = 'schedule'
    _rec_name = 'hour'

    hour = fields.Float('Hour', digits=(16, 2))

    @api.multi
    def name_get(self):
        result = []
        for line in self:
            hour = int(line.hour)
            minutes = int((line.hour-int(line.hour))*60)
            complete = str(hour).zfill(2) + ':' + str(minutes).zfill(2)
            result.append(tuple([line.id, complete]))
        return result
