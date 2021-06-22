# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _
from odoo.exceptions import UserError


class ProductState(models.Model):
    _name = 'product.state'
    _description = "Product states"
    _order = 'sequence'

    name = fields.Char(string='Description', required=True)
    first_state = fields.Boolean(
        string='Is the first state?', default=False)
    sequence = fields.Integer(
        string='Sequence', default=0)
    fold = fields.Boolean(string='Folded in Pipeline')

    def write(self, vals):
        init_state = self.env.ref('product_state_tag.product_first_state')
        if (init_state in self and
                vals.get('sequence', False) != init_state.sequence):
            raise UserError(
                _('You cannot modify the sequence of the first status '
                  'of products.'))
        return super(ProductState, self).write(vals)

    def unlink(self):
        init_state = self.env.ref('product_state_tag.product_first_state')
        for state in self:
            if state == init_state:
                raise UserError(
                    _('You cannot delete the first status of products.'))
        return super(ProductState, self).unlink()
