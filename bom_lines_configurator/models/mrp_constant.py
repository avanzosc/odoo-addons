# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class MrpConstant(models.Model):

    _name = 'mrp.constant'

    name = fields.Char(string='Name', required=True)
    value = fields.Float(string='Value', required=True)
