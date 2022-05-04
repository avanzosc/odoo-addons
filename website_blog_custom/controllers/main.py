
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_blog.controllers.main import WebsiteBlog


class WebsiteBlog(WebsiteBlog):

    @http.route()
    def blogs(self, page=1, **post):
        res = super(WebsiteBlog, self).blogs(page, **post)
        domain = request.website.website_domain()
        Blog = request.env['blog.blog']
        blogs = Blog.search(domain)
        res.qcontext.update({'blogs': blogs})
        return request.render("website_blog_custom.latest_blogs_custom",
                              res.qcontext)

    @http.route()
    def blog(self, blog=None, tag=None, page=1, **opt):
        res = super(WebsiteBlog, self).blog(blog, tag, page, **opt)
        posts = request.env['blog.post'].sudo().search([
            ('blog_id', '=', blog.id)
        ])
        if posts and len(posts) == 1:
            return redirect('/blog/%s/post/%s' % (slug(blog), slug(posts)))
        return res
