# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class Schedule(models.Model):
    _name = 'schedule'
    _rec_name = 'hour'

    hour = fields.Float('Hour', digits=(16, 2))
