# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    block = fields.Boolean(default=False)

    @api.multi
    def block_compute(self):
        self.block = not self.block
