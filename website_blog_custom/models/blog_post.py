
from odoo import fields, models


class BlogPost(models.Model):
    _inherit = "blog.post"

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary("Image", attachment=True,
        help="This field holds the image showed on the external "
             "layout of this post, limited to 1024x1024px",)
