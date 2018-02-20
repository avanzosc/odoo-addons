# -*- coding: utf-8 -*-
# (c) 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class MailMessage(models.Model):
    _inherit = 'mail.message'

    active = fields.Boolean(string='Active', default=True)
