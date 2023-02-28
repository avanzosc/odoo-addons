
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def recalc_line_description(self):
        for line in self.mapped('order_line'):
            line.name = line.get_sale_order_line_multiline_description_sale(line.product_id)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_sale_order_line_multiline_description_variants(self):
        res = super()._get_sale_order_line_multiline_description_variants()
        for record in self.filtered(lambda s: s.product_id.attribute_value_ids):
            show_attibutes = record.product_id.attribute_value_ids.filtered(lambda a: a.attr_display)
            if show_attibutes:
                display_name = '\n'
                for attribute in show_attibutes:
                    attr_val = '%s: %s \n' % (attribute.attribute_id.name, attribute.name)
                    display_name += attr_val
                res = display_name
        return res
