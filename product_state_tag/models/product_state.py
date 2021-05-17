# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _
from odoo.exceptions import UserError


class ProductState(models.Model):
    _name = 'product.state'
    _description = "Product states"

    name = fields.Char(string='Description', required=True)
    first_state = fields.Boolean(
        string='Is the first state?', default=False)
    fold = fields.Boolean(string='Folded in Pipeline')

    def unlink(self):
        init_state = self.env.ref('product_state_tag.product_first_state')
        for state in self:
            if state == init_state:
                raise UserError(
                    _('You cannot delete the first status of products.'))
        return super(ProductState, self).unlink()
