# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_line = fields.Many2one(store=True)
