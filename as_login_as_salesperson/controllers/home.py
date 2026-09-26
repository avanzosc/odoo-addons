# Part of Atharva Systems. See LICENSE file for full copyright and licensing details.
from werkzeug.utils import redirect

from odoo import _, http
from odoo.http import request
from odoo.service import security

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.web.controllers.home import Home


class PortalHome(Home):
    @http.route(["/web/login/login_as_another"], type="http", auth="user", website=True)
    def portal_login_as_another_user(self, user_id=0, **kw):
        uid = request.env.user.id
        request.session.update({"sale_person_id": 0})
        if user_id:
            uid = request.env.user.id
            user = (
                request.env["res.users"]
                .sudo()
                .search([("id", "=", int(user_id))], limit=1)
            )
            available_users = request.env.user.sudo().available_portal_user_ids
            sale_person_id = request.env.user.id
            if available_users and user:
                for portal_user in available_users:
                    if user.id == portal_user.user_id.id:
                        uid = request.session.uid = user.id

                        break

            # invalidate session token cache as we've changed the uid
            request.env["res.users"].clear_caches()
            request.session.session_token = security.compute_session_token(
                request.session, request.env
            )
            request.session.update({"sale_person_id": sale_person_id})
        return redirect(self._login_redirect(uid))


class PortalSalesPerson(CustomerPortal):
    @http.route(
        ["/my/customers", "/my/customers/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_customers(self, search="", page=1, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Users = request.env["res.users"]
        user = request.env["res.users"].sudo().browse(request.uid)
        user_list = []
        if user.available_portal_user_ids and user.is_login_saleperson:
            for portal_user in user.available_portal_user_ids:
                if portal_user.user_id and portal_user.user_id.id not in user_list:
                    if not search:
                        user_list.append(portal_user.user_id.id)
                    if search:
                        search_str = search.lower()
                        name = portal_user.user_id.name.lower()
                        login = portal_user.user_id.login.lower()
                        if search_str in name or search_str in login:
                            user_list.append(portal_user.user_id.id)

        if user:
            tuple_users = tuple(i for i in user_list)
            domain = [("id", "in", tuple_users)]

            searchbar_sortings = {
                "name": {"label": _("Name"), "order": "name asc"},
                "id": {"label": _("ID"), "order": "id asc"},
            }
            # default sort by order
            if not sortby:
                sortby = "name"
            order = searchbar_sortings[sortby]["order"]

            # count for pager
            user_count = Users.sudo().search_count(domain)
            # pager
            # searchbar_filters = {
            #'all': {'label': _('All'), 'domain': []},
            # }
            pager = portal_pager(
                url="/my/customers",
                url_args={"sortby": sortby, "search": search},
                total=user_count,
                page=page,
                step=self._items_per_page,
            )
            # content according to pager and archive selected
            users = Users.sudo().search(
                domain, order=order, limit=self._items_per_page, offset=pager["offset"]
            )
            values.update(
                {
                    "users": users,
                    "page_name": "customers",
                    "pager": pager,
                    "default_url": "/my/customers",
                    "search": search,
                }
            )
            return request.render("as_login_as_salesperson.portal_my_customers", values)
