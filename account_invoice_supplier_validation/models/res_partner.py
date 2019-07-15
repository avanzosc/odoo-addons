# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    hr_department = fields.Many2one(comodel_name='hr.department',
                                    string='Department')
