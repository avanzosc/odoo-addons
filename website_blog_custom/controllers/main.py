
from odoo import http
from odoo.http import request
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
