# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import fields, models


class PurchaseOrderCondition(models.Model):
    _name = 'purchase.order.condition'
    _inherit = ['order.condition']
    _description = 'Purchase Order Condition'
    _order = 'condition_id, purchase_id'

    purchase_id = fields.Many2one(
        comodel_name='purchase.order', string='Purchase Order', required=True)
