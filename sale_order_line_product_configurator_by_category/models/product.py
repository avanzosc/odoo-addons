# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    restricted_products = fields.Many2many(
        comodel_name="product.product",
        relation="product_restricted_product_product_rel",
        column1="restricted_product_id",
        column2="product_id", string="Restricted Products",
        compute="_compute_restricted_products")
    restricted_by = fields.Many2many(related="categ_id.restricted_by")
    restricted_by_products = fields.Many2many(
        comodel_name="product.product",
        relation="product_restriction_product_product_rel",
        column1="restriction_product_id",
        column2="product_id", string="Restricted by Products",
        )
    force_restrict_copy = fields.Boolean(string="Force Copy")

    @api.depends('restricted_by_products')
    def _compute_restricted_products(self):
        for product in self:
            products = self.search([
                ('restricted_by_products', '=', product.id)])
            product.restricted_products = [(6, 0, products._ids)]

    @api.multi
    def button_clear_restrictions(self):
        for product in self:
            product.restricted_by_products = [(5,)]

    @api.multi
    def button_copy_to_siblings(self):
        for product in self:
            restriction_ids = product.restricted_by_products._ids
            force = product.force_restrict_copy
            variants = product.product_tmpl_id.product_variant_ids \
                .filtered(lambda x: x.id != product.id)
            if not force:
                variants = variants.filtered(lambda x:
                                             not x.restricted_by_products)
            variants.write(
                {'restricted_by_products': [(6, 0, restriction_ids)]})
            if product.force_restrict_copy:
                product.force_restrict_copy = False

    @api.multi
    def button_category_restrict_products(self):
        for product in self:
            restrict_category = product.categ_id.restricted_by.ids
            categ_products = product.search([('categ_id', 'child_of',
                                              restrict_category)])
            for categ_product in categ_products:
                product.restricted_by_products = [(4, categ_product.id)]
