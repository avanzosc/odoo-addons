# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    shop_variant_split = fields.Boolean(
        string="Split variants in shop",
        help="In the online shop, show a separate product for each value of "
        "the attributes with 'Split variants in shop'.",
    )

    def _get_shop_split_variants(self, attribute_value_ids=()):
        selected_values = set(attribute_value_ids)
        result = {}
        for template in self.filtered("shop_variant_split"):
            if template.id in result:
                continue
            split_lines = template.valid_product_template_attribute_line_ids.filtered(
                lambda line: line.attribute_id.shop_variant_split
                and line.attribute_id.create_variant != "no_variant"
            )
            if not split_lines:
                continue
            variants_by_values = {}
            for variant in template.product_variant_ids:
                split_values = variant.product_template_attribute_value_ids.filtered(
                    lambda value, lines=split_lines: value.attribute_line_id in lines
                )
                if any(
                    value.product_attribute_value_id.id not in selected_values
                    and selected_values & set(value.attribute_line_id.value_ids.ids)
                    for value in split_values
                ):
                    continue
                variants_by_values.setdefault(frozenset(split_values.ids), variant)
            if variants_by_values:
                result[template.id] = list(variants_by_values.values())
        return result

    def _get_shop_split_variant(self):
        self.ensure_one()
        variant_id = self.env.context.get("shop_split_variant_id")
        if not variant_id:
            return self.env["product.product"]
        return self.product_variant_ids.filtered(
            lambda variant: variant.id == variant_id
        )

    def _get_shop_split_prices(self):
        combination_info = self._get_combination_info()
        prices = {"price_reduce": combination_info["price"]}
        if combination_info["has_discounted_price"]:
            prices["base_price"] = combination_info["list_price"]
        elif combination_info["compare_list_price"]:
            prices["base_price"] = combination_info["compare_list_price"]
        return prices

    def _get_first_possible_variant_id(self):
        variant = self._get_shop_split_variant()
        if variant:
            return variant.id
        return super()._get_first_possible_variant_id()

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1.0,
        parent_combination=False,
        only_template=False,
    ):
        if not (combination or product_id or only_template):
            variant = self._get_shop_split_variant()
            if variant:
                combination = variant.product_template_attribute_value_ids
                product_id = variant.id
        return super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            parent_combination=parent_combination,
            only_template=only_template,
        )
