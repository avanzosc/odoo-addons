
from odoo import fields, http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_blog.controllers.main import WebsiteBlog


class WebsiteBlog(WebsiteBlog):

    @http.route()
    def blogs(self, page=1, **post):
        res = super(WebsiteBlog, self).blogs(page, **post)
        values = {}
        logged_user = request.env['res.users'].browse(request.uid)
        search_ids = logged_user.partner_id.child_ids.ids
        search_ids.append(logged_user.partner_id.id)

        domain = request.website.website_domain()

        domain += [
            ('invited_partner_ids', 'in', search_ids),
        ]

        BlogPost = request.env['blog.post']
        total = BlogPost.search_count(domain)

        pager = request.website.pager(
            url='/blog',
            total=total,
            page=page,
            step=self._blog_post_per_page,
        )
        posts = BlogPost.search(domain, offset=(page - 1) * self._blog_post_per_page, limit=self._blog_post_per_page)

        values.update({
            'pager': pager,
            'posts': posts
        })
        res.qcontext.update(values)
        return res
