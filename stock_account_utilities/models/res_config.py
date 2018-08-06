# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class StockConfigSettings(models.TransientModel):
    _inherit = 'stock.config.settings'

    group_picking_invoicing = fields.Boolean(
        string="Invoice to be invoiced pickings in any state",
        implied_group='stock_account_utilities.group_picking_invoicing',
        help="""Allows to invoice a picking in any state.""")
