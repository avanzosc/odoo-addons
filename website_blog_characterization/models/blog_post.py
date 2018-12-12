# Copyright 2018 Gotzon Imaz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, tools


class BlogPost(models.Model):
    _inherit = 'blog.post'

    area_ids = fields.Many2many(
        string='Areas', comodel_name='res.partner.area',
        relation='rel_blog_area', column1='blog_id',
        column2='area_id', copy=False)
    committee_ids = fields.Many2many(
        string='Committees', comodel_name='res.committee',
        relation='rel_blog_committee', column1='blog_id',
        column2='committee_id', copy=False)
    team_ids = fields.Many2many(
        string='Teams', comodel_name='res.team',
        relation='rel_blog_team', column1='blog_id',
        column2='team_id', copy=False)
    structure_ids = fields.Many2many(
        string='Structures', comodel_name='res.structure',
        relation='rel_blog_structure', column1='blog_id',
        column2='structure_id', copy=False)
    main_contact = fields.Boolean(string='Main Contact')
    assembly = fields.Boolean(string='Assembly')
    joint = fields.Boolean(string='Joint')
    bidding = fields.Boolean(string='Bidding')


class BlogTag(models.Model):
    _inherit = 'blog.tag'

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary(
        string="Image", attachment=True,
        help="This field holds the image used as avatar for this contact, "
             "limited to 1024x1024px",)
    image_medium = fields.Binary(
        string="Medium-sized image", attachment=True,
        help="Medium-sized image of this contact. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary(
        string="Small-sized image", attachment=True,
        help="Small-sized image of this contact. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        result = super(BlogTag, self).write(vals)
        return result

    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        tag = super(BlogTag, self).create(vals)
        return tag
