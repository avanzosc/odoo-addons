
from odoo import api, fields, models


class WizCreateProdVariant(models.TransientModel):
    _name = "wiz.product.product.create"
    _description = "Wizard to Create Product Variants Manually"

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template',
        required=True)
    parent_product_template_attribute_value_ids = fields.Many2many(
        'product.template.attribute.value', string="Product Template Attribute Values",
        compute="_compute_product_tmpl_att_values", store=True)
    product_template_attribute_value_ids = fields.Many2many(
        'product.template.attribute.value',
        'wiz_prod_val_rel', 'wiz_id', 'val_id',
        string='Product Attributes',
        required=True)
    default_code = fields.Char('Internal Reference', index=True)
    barcode = fields.Char('Barcode')
    lst_price = fields.Float('Public Price')
    product_variant_count = fields.Integer('Variant Count', related='product_tmpl_id.product_variant_count')

    standard_price = fields.Float('Cost')

    @api.depends('product_tmpl_id', 'product_tmpl_id.attribute_line_ids')
    def _compute_product_tmpl_att_values(self):
        for record in self:
            # domain =
            # existing_products = record.product_tmpl_id.product_variant_ids
            # if existing_products:
            #     existing_variant_combinations = existing_products.mapped(
            #         'product_template_attribute_value_ids')
            #     domain = domain.append([
            #         ('id', 'not in', existing_variant_combinations)])

            att_values = self.env['product.template.attribute.value'].search([
                ('attribute_line_id', 'in',
                  record.product_tmpl_id.attribute_line_ids.ids)
            ])
            record.parent_product_template_attribute_value_ids = att_values

    def default_get(self, var_fields):
        context = self.env.context
        res = super(WizCreateProdVariant, self).default_get(var_fields)
        product_tmpl_id = context.get('active_id')
        res.update({
            'product_tmpl_id': product_tmpl_id
        })
        return res

    def action_create_product_variant(self):
        self.ensure_one()

        product = self.env['product.product'].create({
            'product_tmpl_id': self.product_tmpl_id.id,
            'product_template_attribute_value_ids':
                self.product_template_attribute_value_ids.ids,
            'default_code': self.default_code,
            'barcode': self.barcode,
            'lst_price': self.lst_price,
            'standard_price': self.standard_price,
        })

        return True
