
from odoo import fields, models


class BlogPost(models.Model):
    _inherit = "blog.post"

    education_center_ids = fields.Many2many(
        related="blog_id.education_center_ids")
    education_course_ids = fields.Many2many(
        related="blog_id.education_course_ids")
    education_group_ids = fields.Many2many(
        related="blog_id.education_group_ids")
    education_category_ids = fields.Char(
        related="blog_id.education_category_ids")

    invited_partner_ids = fields.Many2many(
        related="blog_id.invited_partner_ids")
    invited_count = fields.Integer(related="blog_id.invited_count")
