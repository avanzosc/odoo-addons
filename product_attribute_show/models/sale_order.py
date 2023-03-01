
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
                for attribute in show_attibutes:
                    attr_val = '%s: %s ' % (attribute.attribute_id.name, attribute.name)
                    if attribute.is_custom:
                        for custom_value in record.product_custom_attribute_value_ids.filtered(
                                lambda a: a.attribute_value_id.id == attribute.id):
                            attr_val += '%s ' % custom_value.display_name
                    display_name += (attr_val + '\n')
                res = display_name
        return res
