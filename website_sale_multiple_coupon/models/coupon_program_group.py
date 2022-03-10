from odoo import api, fields, models


class CouponProgramGroup(models.Model):
    _name = "coupon.program.group"

    name = fields.Char('Group name')
    coupon_programs = fields.Many2many(
        'coupon.program', 'coupon_program_group_rel', 'group_id', 'program_id',
        string='Coupon programs'
    )
    apply_always = fields.Boolean('Apply always')
