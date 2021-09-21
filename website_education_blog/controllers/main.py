
from odoo import http
from odoo.http import request
from odoo.addons.website_blog.controllers.main import WebsiteBlog


class WebsiteBlog(WebsiteBlog):

    @http.route()
    def blogs(self, page=1, **post):
        res = super(WebsiteBlog, self).blogs(page, **post)
        values = {}
        logged_user = request.env['res.users'].browse(request.uid)
        logged_partner = logged_user.partner_id
        if logged_partner.educational_category == 'student':
            search_partners = logged_partner
        else:
            search_partners = logged_partner.progenitor_child_ids

        domain = request.website.website_domain()
        domain += [
            ('website_published', '=', True),
            '|',
            ('education_center_ids', '=', False),
            ('education_center_ids', '=',
             search_partners.mapped('current_center_id').ids),
            '|',
            ('education_course_ids', '=', False),
            ('education_course_ids', '=',
             search_partners.mapped('current_course_id').ids),
            '|',
            ('education_group_ids', '=', False),
            ('education_group_ids', '=',
             search_partners.mapped('current_group_id').ids),
        ]

        BlogPost = request.env['blog.post'].sudo()
        total = BlogPost.search_count(domain)

        pager = request.website.pager(
            url='/blog',
            total=total,
            page=page,
            step=self._blog_post_per_page,
        )
        posts = BlogPost.search(
            domain, offset=(page - 1) * self._blog_post_per_page,
            limit=self._blog_post_per_page)

        values.update({
            'pager': pager,
            'posts': posts
        })
        res.qcontext.update(values)
        return res
