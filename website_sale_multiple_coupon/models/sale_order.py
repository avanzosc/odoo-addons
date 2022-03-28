from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _update_existing_reward_lines(self):
        super(SaleOrder, self)._update_existing_reward_lines()

        self.ensure_one()
        order = self
        applied_programs = order._get_applied_programs_with_rewards_on_current_order()

        for program in applied_programs.filtered(
                lambda r: r.apply_on_total and r.discount_percentage):
            lines = order.order_line.filtered(
                lambda line: line.product_id == program.discount_line_product_id)

            for line in lines:
                prev_amount_total = self.get_previous_line_amount_total(order, line)
                discount = program.discount_percentage/100
                values = {
                    'price_unit':
                        - abs(float(prev_amount_total*discount))
                    }
                line.write(values)

    def get_previous_line_amount_total(self, order, last_line):
        prev_amount_total = 0.0
        for line in order.order_line:
            if line == last_line:
                break
            prev_amount_total = prev_amount_total + line.price_unit
        return prev_amount_total
