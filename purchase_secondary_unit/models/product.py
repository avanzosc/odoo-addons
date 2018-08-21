# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, exceptions, fields, models
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uop_id = fields.Many2one(
        comodel_name='product.uom', string='Secondary Unit of Purchase',
        help='Specify a unit of measure here if purchasing is made in another'
        ' unit of measure category than inventory. Keep empty to use the'
        ' default unit of measure.')
    uop_coeff = fields.Float(
        string='Purchase Unit of Measure -> 2UoP Coeff',
        digits=dp.get_precision('Product UoP'),
        help='Coefficient to convert default Purchase Unit of Measure to'
        ' Secondary Unit of Purchase\n uop = uom * coeff', default=1.0)

    @api.constrains('uop_id')
    def _check_uop_id(self):
        for tmpl in self.filtered('uop_id'):
            if tmpl.uom_po_id.category_id != tmpl.uop_id.category_id:
                raise exceptions.ValidationError(
                    'Purchase Unit of Measure and Secondary Unit of Purchase '
                    'belong to different Category! ')
