# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_price_by_pricelist_ids = fields.One2many(
        string="Product price by pricelist", inverse_name="product_id",
        comodel_name="product.price.by.pricelist")
    last_date_price_by_pricelist = fields.Date(
        string="Last date price by pricelist")

    def put_price_unit_by_pricelist_in_products(self):
        pricelists = self.env['product.pricelist'].search([])
        cond = ['|', ("last_date_price_by_pricelist", "=", False),
                ("last_date_price_by_pricelist", "!=",
                 fields.Date.context_today(self))]
        products = self.env['product.product'].search(cond)
        for product in products:
            product.with_context(
                product_pricelists=pricelists).calculate_price_by_pricelist()
            product.last_date_price_by_pricelist = (
                fields.Date.context_today(self))
            self._cr.commit()

    def calculate_price_by_pricelist(self):
        product_obj = self.env["product.product"]
        product_price_by_pricelist_obj = self.env["product.price.by.pricelist"]
        product_pricelists = product_obj.get_product_pricelists()
        for product in self:
            for product_pricelist in product_pricelists:
                price_unit = product.get_product_price_by_pricelist(
                    product_pricelist)
                product_pricepricelist = product.product_price_by_pricelist_ids
                product_price_by_pricelist = product_pricepricelist.filtered(
                    lambda x: x.pricelist_id == product_pricelist)
                if product_price_by_pricelist:
                    vals = product._vals_for_product_price_by_pricelist(
                        price_unit)
                    product_price_by_pricelist.sudo().write(vals)
                else:
                    vals = product._vals_for_product_price_by_pricelist(
                        price_unit, product, product_pricelist)
                    product_price_by_pricelist_obj.sudo().create(vals)

    def get_product_pricelists(self):
        if ("product_pricelists" in self.env.context and
                self.env.context.get("product_pricelists", False)):
            return self.env.context.get("product_pricelists")
        else:
            return self.env['product.pricelist'].search([])

    def get_product_price_by_pricelist(self, product_pricelist):
        account_tax_obj = self.env['account.tax']
        result = self._get_display_price(product_pricelist)
        price_unit = account_tax_obj._fix_tax_included_price_company(
            result, self.taxes_id, self.taxes_id, self.company_id)
        return price_unit

    @api.multi
    def _get_display_price(self, product_pricelist):
        final_price, rule_id = product_pricelist.get_product_price_rule(
                self, 1.0, self.env.user.partner_id)
        base_price, currency = self._get_real_price_currency(
                rule_id, 1, self.uom_id)
        return max(base_price, final_price)

    def _get_real_price_currency(self, rule_id, qty, uom):
        PricelistItem = self.env['product.pricelist.item']
        field_name = 'lst_price'
        currency_id = None
        product_currency = self.currency_id
        product = self
        if rule_id:
            pricelist_item = PricelistItem.browse(rule_id)
            if (pricelist_item.pricelist_id.discount_policy ==
                    'without_discount'):
                while (pricelist_item.base == 'pricelist' and
                        pricelist_item.base_pricelist_id and
                        pricelist_item.base_pricelist_id.discount_policy ==
                        'without_discount'):
                    base_pricelist_id = pricelist_item.base_pricelist_id
                    price, rule_id = base_pricelist_id.with_context(
                        uom=uom.id).get_product_price_rule(
                            self, qty, self.env.user.partner_id)
                    pricelist_item = PricelistItem.browse(rule_id)
            if pricelist_item.base == 'standard_price':
                field_name = 'standard_price'
                product_currency = self.cost_currency_id
            elif (pricelist_item.base == 'pricelist' and
                    pricelist_item.base_pricelist_id):
                field_name = 'price'
                product = self.with_context(
                    pricelist=pricelist_item.base_pricelist_id.id)
                product_currency = pricelist_item.base_pricelist_id.currency_id
            currency_id = pricelist_item.pricelist_id.currency_id
        if not currency_id:
            currency_id = product_currency
            cur_factor = 1.0
        else:
            if currency_id.id == product_currency.id:
                cur_factor = 1.0
            else:
                cur_factor = currency_id._get_conversion_rate(
                    product_currency, currency_id, product.company_id,
                    fields.Datetime.now())
        product_uom = product.uom_id.id
        if uom and uom.id != product_uom:
            # the unit price is in a different uom
            uom_factor = uom._compute_price(1.0, product.uom_id)
        else:
            uom_factor = 1.0
        return product[field_name] * uom_factor * cur_factor, currency_id

    def _vals_for_product_price_by_pricelist(self, price_unit,
                                             product=False,
                                             product_pricelist=False):
        vals = {'price_unit': price_unit}
        if product:
            vals["product_id"] = product.id
        if product_pricelist:
            vals["pricelist_id"] = product_pricelist.id
        return vals
