# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    cap_type_id = fields.Many2one(
        comodel_name='stock.picking.type', string='Tipo captura')
