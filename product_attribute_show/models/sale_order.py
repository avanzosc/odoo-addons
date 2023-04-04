
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def recalc_line_description(self, model=None):
        for line in self.mapped('order_line'):
            line.name = line.get_sale_order_line_multiline_description_sale(line.product_id, model=model)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def get_filtered_attribute_order_lines(self):
        return self.filtered(lambda s: s.product_id.attribute_value_ids)

    def _get_sale_order_line_multiline_description_variants(self):
        res = super()._get_sale_order_line_multiline_description_variants()
        for record in self.get_filtered_attribute_order_lines():
            show_attibutes = record.product_id.attribute_value_ids.filtered(lambda a: a.attr_display)
            if show_attibutes:
                display_name = '\n'
                res = self._concat_categ_attributes(record, show_attibutes, display_name)
        return res

    def _concat_categ_attributes(self, line, attribute_values, origin_str=''):
        attributes = attribute_values.mapped('attribute_id')
        categs = attributes.mapped('category_id')
        if not categs:
            origin_str += self._concat_attributes(line, attribute_values, origin_str=origin_str)
        else:
            for category in categs:
                categ_attr_vals = attributes.filtered(
                    lambda a: a.category_id.id == category.id).mapped('value_ids').filtered(
                    lambda v: v.id in attribute_values.ids)
                origin_str += self._concat_attributes(line, categ_attr_vals, origin_str='\n', separator=',')
            no_categ_attr_vals = attributes.filtered(lambda a: not a.category_id).mapped('value_ids').filtered(
                    lambda v: v.id in attribute_values.ids)
            origin_str += self._concat_attributes(line, no_categ_attr_vals, origin_str='\n')
        return origin_str

    def _concat_attributes(self, line, attribute_values, origin_str='', separator='\n'):
        i = 0
        for attribute in attribute_values:
            attr_val = '%s:%s' % (attribute.attribute_id.name, attribute.name)
            if attribute.is_custom:
                for custom_value in line.product_custom_attribute_value_ids.filtered(
                                lambda a: a.attribute_value_id.id == attribute.id):
                    attr_val += '%s' % custom_value.display_name
            origin_str += attr_val
            i += 1
            if i < len(attribute_values):
                origin_str += separator
        return origin_str

    def get_sale_order_line_multiline_description_sale(self, product, model=None):
        return product.get_product_multiline_description_sale(model=model) + self._get_sale_order_line_multiline_description_variants()
