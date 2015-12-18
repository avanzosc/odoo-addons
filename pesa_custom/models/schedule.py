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
        name = self._rec_name
        if name in self._fields:
            convert = self._fields[name].convert_to_display_name
            for line in self:
                complete_hour = str(int(line.hour)).zfill(2) + ':' + (
                    str(int((line.hour-int(line.hour))*60)).zfill(2))
                result.append((line.id, convert(complete_hour, line)))
        else:
            for line in self:
                complete_hour = str(int(line.hour)).zfill(2) + ':' + (
                    str(int((line.hour-int(line.hour))*60)).zfill(2))
                result.append((line.id, "%s,%s" % (complete_hour, line.id)))
        return result
