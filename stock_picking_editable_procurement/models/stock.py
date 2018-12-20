# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    group_id = fields.Many2one(readonly=False)
