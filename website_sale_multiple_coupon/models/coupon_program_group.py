from odoo import fields, models


class CouponProgramGroup(models.Model):
    _name = "coupon.program.group"

    name = fields.Char("Group name")
    coupon_programs = fields.Many2many(
        "coupon.program",
        "coupon_program_group_rel",
        "group_id",
        "program_id",
        string="Coupon programs",
    )
    partner_category_ids = fields.Many2many(
        "res.partner.category",
        "partner_category_coupon_program_group_rel",
        "group_id",
        "partner_id",
        string="Partner categories",
    )
    apply_always = fields.Boolean("Apply always")
