# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        product = super(ProductProduct, self).create(vals)
        product.put_taxes_in_others_companies(self.env.user.company_id)
        return product

    def product_put_tax_multicompany(self):
        companies = self.env['res.company'].sudo().search([])
        for company in companies:
            products = self.env['product.product'].with_context(
                force_company=company).sudo().search([])
            for product in products:
                product.put_taxes_in_others_companies(company)

    def put_taxes_in_others_companies(self, my_company):
        companies = self.company_ids
        original_company = my_company
        if self.company_ids and len(self.company_ids) > 1:
            if self.taxes_id:
                for company in companies.filtered(
                        lambda x: x.id != original_company.id):
                    my_company = self.env['res.company'].sudo().browse(
                        company.id)
                    if my_company.account_sale_tax_id:
                        tax = my_company.account_sale_tax_id
                        self._cr.execute("""SELECT COUNT(*)
                                        FROM product_taxes_rel
                                        WHERE prod_id = %s AND tax_id = %s""",
                                         (self.id,
                                          my_company.account_sale_tax_id.id))
                        found = self._cr.fetchone()[0]
                        if not found:
                            self._cr.execute("""INSERT INTO product_taxes_rel
                                            (prod_id, tax_id)
                                            VALUES (%s, %s)""", (self.id,
                                                                 tax.id))
            if self.supplier_taxes_id:
                for company in companies.filtered(
                        lambda x: x.id != original_company.id):
                    my_company = self.env['res.company'].sudo().browse(
                        company.id)
                    if my_company.account_purchase_tax_id:
                        tax = my_company.account_purchase_tax_id
                        self._cr.execute("""SELECT COUNT(*)
                                        FROM product_supplier_taxes_rel
                                        WHERE prod_id = %s AND tax_id = %s""",
                                         (self.id, tax.id))
                        found = self._cr.fetchone()[0]
                        if not found:
                            self._cr.execute("""INSERT INTO
                                            product_supplier_taxes_rel
                                            (prod_id, tax_id)
                                            VALUES (%s, %s)""", (self.id,
                                                                 tax.id))
