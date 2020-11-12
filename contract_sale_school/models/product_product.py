# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_real_price_currency(
            self, rule_id, qty, uom, pricelist_id, date=False,
            company_id=False):
        """Retrieve the price before applying the pricelist
            :param float qty: total quantity of product
            :param tuple price_and_rule: tuple(price, suitable_rule)
                coming from pricelist computation
            :param obj uom: unit of measure
            :param integer pricelist_id: pricelist id"""
        self.ensure_one()
        product = self
        PricelistItem = self.env['product.pricelist.item']
        field_name = 'lst_price'
        currency_id = None
        product_currency = self.currency_id
        if rule_id:
            pricelist_item = PricelistItem.browse(rule_id)
            if (pricelist_item.pricelist_id.discount_policy ==
                    'without_discount'):
                while (pricelist_item.base == 'pricelist' and
                       pricelist_item.base_pricelist_id and
                       (pricelist_item.base_pricelist_id.discount_policy ==
                        'without_discount')):
                    price, rule_id = (
                        pricelist_item.base_pricelist_id.with_context(
                            uom=uom.id).get_product_price_rule(
                                self, qty, self.order_id.partner_id))
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
                    product_currency, currency_id,
                    company_id or self.env.user.company_id,
                    date or fields.Date.today())

        product_uom = self.env.context.get('uom') or self.uom_id.id
        if uom and uom.id != product_uom:
            # the unit price is in a different uom
            uom_factor = uom._compute_price(1.0, product.uom_id)
        else:
            uom_factor = 1.0

        return product[field_name] * uom_factor * cur_factor, currency_id
