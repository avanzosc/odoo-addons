# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class ProductTemplateAttributeValue(models.Model):
    _inherit = 'product.template.attribute.value'

    @api.multi
    @api.depends(
        'product_tmpl_id', 'product_attribute_value_id',
        'product_tmpl_id.product_variant_ids',
        'product_tmpl_id.product_variant_ids.default_code',
        'product_tmpl_id.product_variant_ids.attribute_value_ids')
    def _compute_default_code(self):
        for value in self.filtered(lambda x: x.product_tmpl_id):
            default_code = ''
            for product in value.product_tmpl_id.product_variant_ids:
                if (len(product.attribute_value_ids) == 1 and
                    value.product_attribute_value_id in
                        product.attribute_value_ids):
                    default_code = product.default_code
                    break
            value.default_code = default_code

    def _compute_quantity_on_hand(self):
        for value in self.filtered(lambda x: x.product_tmpl_id):
            quantity_on_hand = 0.0
            for product in value.product_tmpl_id.product_variant_ids:
                if (len(product.attribute_value_ids) == 1 and
                    value.product_attribute_value_id in
                        product.attribute_value_ids):
                    quantity_on_hand = (
                        product.qty_available - product.outgoing_qty)
                    break
            value.quantity_on_hand = quantity_on_hand

    default_code = fields.Char(
        string='Internal Reference', compute='_compute_default_code',
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
