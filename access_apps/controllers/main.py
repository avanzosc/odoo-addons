from odoo import SUPERUSER_ID, http
from odoo.http import request

from odoo.addons.web_settings_dashboard.controllers.main import WebSettingsDashboard


class WebSettingsDashboardCustom(WebSettingsDashboard):
    @http.route("/web_settings_dashboard/data", type="json", auth="user")
    def web_settings_dashboard_data(self, **kw):
        has_access_to_apps = request.env["res.users"].has_group(
            "access_apps.group_allow_apps"
        )
        # issue: due to unknown reason has_group is always invoked with superuser as uid param in new API
        # has_access_to_apps = request.env.user.has_group('access_apps.group_allow_apps')
        request.env.uid = SUPERUSER_ID
        res = super(WebSettingsDashboardCustom, self).web_settings_dashboard_data(**kw)
        res["has_access_to_apps"] = has_access_to_apps
        return res
