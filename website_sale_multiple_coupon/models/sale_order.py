from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_new_no_code_promo_reward_lines(self):
        '''Apply new programs that are applicable'''
        self.ensure_one()
        order = self
        programs = order._get_applicable_no_code_promo_program()
        programs = programs._keep_only_most_interesting_auto_applied_global_discount_program(order=order)
        for program in programs:
            # VFE REF in master _get_applicable_no_code_programs already filters programs
            # why do we need to reapply this bunch of checks in _check_promo_code ????
            # We should only apply a little part of the checks in _check_promo_code...
            error_status = program._check_promo_code(order, False)
            if not error_status.get('error'):
                if program.promo_applicability == 'on_next_order':
                    order.state != 'cancel' and order._create_reward_coupon(program)
                elif program.discount_line_product_id.id not in self.order_line.mapped('product_id').ids:
                    self.write({'order_line': [(0, False, value) for value in self._get_reward_line_values(program)]})
                order.no_code_promo_program_ids |= program

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
        for line in order.order_line.filtered(lambda l: l.id != last_line.id):
            prev_amount_total = prev_amount_total + line.price_subtotal
        return prev_amount_total
