# -*- coding: utf-8 -*-
# Copyright 2018 alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    notes = fields.Text(string='Notes')
