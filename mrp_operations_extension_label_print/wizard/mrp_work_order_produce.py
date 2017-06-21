# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class MrpWorkOrderProduce(models.TransientModel):

    _inherit = "mrp.work.order.produce"

    ul_id = fields.Many2one(comodel_name='product.ul', string='Package Type')
    ul_qty = fields.Integer(string='Package Quantity')
