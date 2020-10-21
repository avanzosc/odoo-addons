# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields
from odoo.addons import decimal_precision as dp


class ProductTemplateAttributeValue(models.Model):
    _inherit = 'product.template.attribute.value'

    def _compute_quantity_on_hand(self):
        for value in self.filtered(lambda x: x.product_tmpl_id):
            if len(value.product_tmpl_id.product_variant_ids) == 1:
                variant = value.product_tmpl_id.product_variant_ids[0]
                value.quantity_on_hand = (
                    variant.qty_available - variant.outgoing_qty)

    default_code = fields.Char(
        string='Internal Reference', related='product_tmpl_id.default_code',
        copy=False, store=True)
    product_tmpl_categ_id = fields.Many2one(
        string='Category', comodel_name='product.category', copy=False,
        related='product_tmpl_id.categ_id', store=True)
    quantity_on_hand = fields.Float(
        string='Quantity on hand', compute='_compute_quantity_on_hand',
        digits=dp.get_precision('Product Unit of Measure'))
    company_id = fields.Many2one(
        string='Company', comodel_name='res.company', store=True,
        related='product_tmpl_id.company_id')
