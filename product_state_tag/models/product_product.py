# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _default_state_id(self):
        cond = [('first_state', '=', True)]
        state = self.env['product.state'].search(cond)
        return state.id

    state_id = fields.Many2one(
        string='State', comodel_name='product.state', ondelete='restrict',
        tracking=True, index=True, copy=False,
        default=lambda self: self._default_state_id())
    product_tag_ids = fields.Many2many(
        string='Product tags', comodel_name='product.tag')
