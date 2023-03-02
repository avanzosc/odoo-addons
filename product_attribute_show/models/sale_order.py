
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def recalc_line_description(self):
        for line in self.mapped('order_line'):
            line.name = line.get_sale_order_line_multiline_description_sale(line.product_id)


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
                res = self._concat_group_attributes(record, show_attibutes, display_name)
        return res

    def _concat_group_attributes(self, line, attribute_values, origin_str=''):
        attributes = attribute_values.mapped('attribute_id')
        groups = self.env['product.attribute.group'].search([
            ('active', '=', True),
            ('product_attribute_ids', 'in', attributes.ids)
        ])
        if not groups:
            origin_str += self._concat_attributes(line, attribute_values, origin_str=origin_str)
        else:
            for group in groups:
                group_attr_vals = group.product_attribute_ids.mapped('value_ids').filtered(
                    lambda a: a.id in attribute_values.ids)
                origin_str += self._concat_attributes(line, group_attr_vals, origin_str='\n', separator=', ')
            all_group_attr_vals = groups.mapped('product_attribute_ids').mapped('value_ids').filtered(
                lambda a: a.id in attribute_values.ids)
            no_group_attrs = attribute_values.filtered(lambda a: a.id not in all_group_attr_vals.ids)
            origin_str += self._concat_attributes(line, no_group_attrs, origin_str='\n')
        return origin_str

    def _concat_attributes(self, line, attribute_values, origin_str='', separator='\n'):
        for attribute in attribute_values:
            attr_val = '%s: %s ' % (attribute.attribute_id.name, attribute.name)
            if attribute.is_custom:
                for custom_value in line.product_custom_attribute_value_ids.filtered(
                                lambda a: a.attribute_value_id.id == attribute.id):
                    attr_val += '%s ' % custom_value.display_name
            origin_str += (attr_val + separator)
        return origin_str
