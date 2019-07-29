# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields

WARNING_MESSAGE = [('no-message', 'No Message'),
                   ('warning', 'Warning'),
                   ('block', 'Blocking Message')]


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    out_picking_warn = fields.Selection(
        selection=WARNING_MESSAGE, required=True, string='Out picking line',
        default='no-message')
    out_picking_warn_msg = fields.Text(
        string='Message for out picking line')
    in_picking_warn = fields.Selection(
        selection=WARNING_MESSAGE, required=True, string='In picking line',
        default='no-message')
    in_picking_warn_msg = fields.Text(
        string='Message for in picking line')
