# -*- coding: utf-8 -*-
# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    quotation_visible = fields.Boolean(string="Quotation visible")
