# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    line = fields.Char(string='Line')
    real_line_id = fields.Many2one(comodel_name='real.line',
                                   string='Real line')
    journey_id = fields.Many2one(comodel_name='journey',
                                    string='Journey')
    schedule_id = fields.Many2one(comodel_name='schedule', string='Schedule')
    driver_id = fields.Many2one(comodel_name='res.users', string='Driver')
    book_number = fields.Integer(string='Book number')
    book_page = fields.Integer(string='Book page')
    service_date = fields.Date(string='Service date')
