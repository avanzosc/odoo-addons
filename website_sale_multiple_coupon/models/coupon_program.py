from odoo import _, api, fields, models
from odoo.http import request


class CouponProgram(models.Model):
    _inherit = "coupon.program"

    apply_always = fields.Boolean('Apply always')

    apply_on_total = fields.Boolean(
        'Apply on total', help="Apply coupon on the total amount of the SO,"
                               " in the SO line sequence order.")

    coupon_program_groups = fields.Many2many(
        'coupon.program.group', 'coupon_program_group_rel', 'program_id',
        'group_id', string='Coupon program Groups')

    def _check_promo_code(self, order, coupon_code):
        message = super(CouponProgram, self)._check_promo_code(order, coupon_code)

        if self._is_global_discount_program() and order._is_global_discount_already_applied():
            message = {}
        return message

    def _check_group_promo_code(self, order, coupon_code, group):
        message = {}
        if order._get_applicable_programs() in group.coupon_programs:
            message = {
                'error': _('Promo group already applied.')}
        # elif self.promo_code and self.promo_code == order.promo_code:
        #     message = {'error': _('The promo code is already applied on this order')}
        # elif self in order.no_code_promo_program_ids:
        #     message = {'error': _('already_applied')}
        elif self.maximum_use_number != 0 and self.order_count >= self.maximum_use_number:
            message = {
                'error': _('Promo code %s has been expired.') % (coupon_code)}
        elif not self._filter_on_mimimum_amount(order):
            message = {'error': _(
                'A minimum of %(amount)s %(currency)s should be purchased to get the reward',
                amount=self.rule_minimum_amount,
                currency=self.currency_id.name
            )}
        elif not self._filter_programs_on_products(order):
            message = {'error': _(
                "You don't have the required product quantities on your sales order. If the reward is same product quantity, please make sure that all the products are recorded on the sales order (Example: You need to have 3 T-shirts on your sales order if the promotion is 'Buy 2, Get 1 Free'.")}
        elif self.promo_applicability == 'on_current_order' and not self.env.context.get(
                'applicable_coupon'):
            applicable_programs = order._get_applicable_programs()
            if self not in applicable_programs:
                message = {'error': _(
                    'At least one of the required conditions is not met to get the reward!')}
        return message

    def _keep_only_most_interesting_auto_applied_global_discount_program(self):
        groups = self.env['coupon.program.group'].search([
            ('apply_always', '=', True)])
        no_group_programs = self.filtered(
            lambda p: p._is_global_discount_program()
                      and p.promo_code_usage == 'no_code_needed'
                      and p not in groups.mapped('coupon_programs')
                      and p.apply_always)

        order = None
        if groups or no_group_programs:
            website = request and getattr(request, 'website', None)
            order = website.sale_get_order() if website else None
            if not order:
                ctx = self.env.context
                params = ctx.get('params') if ctx else None
                if params and params.get('model') == 'sale.order':
                    order_id = params.get('id')
                    order = self.env['sale.order'].browse(order_id)
        if order:
            applicable_programs = no_group_programs
            for group in groups:
                for program in group.coupon_programs.sorted(
                        lambda p: (p.rule_min_quantity, p.rule_minimum_amount),
                        reverse=True):
                    error = program._check_group_promo_code(order, False, group)
                    if not error:
                        applicable_programs = applicable_programs + program
                        break
            return applicable_programs
        return super(CouponProgram, self)._keep_only_most_interesting_auto_applied_global_discount_program()
