import odoo.tests


@odoo.tests.tagged("at_install", "post_install")
class TestUi(odoo.tests.HttpCase):
    def test_01_dashboard_remove(self):
        phantom_env = self.env
        demo_user = phantom_env.ref("base.user_demo")
        system_group = phantom_env.ref("base.group_system")
        allow_apps_group = phantom_env.ref("access_apps.group_allow_apps")
        demo_user.write({"groups_id": [(4, system_group.id)]})
        demo_user.write({"groups_id": [(3, allow_apps_group.id)]})
        url = "/web#menu_id={}&action={}".format(
            phantom_env.ref("web_settings_dashboard.web_dashboard_menu").id,
            phantom_env.ref("web_settings_dashboard.web_settings_dashboard_action").id,
        )
        code = """
                    if ($('.o_web_settings_dashboard_apps').length) {
                        console.log("error", "The apps dashboard is not removed");
                    } else {
                        console.log('ok');
                    }
        """
        self.phantom_js(
            url,
            code,
            "odoo.__DEBUG__.services['access_apps.dashboard'].ready.state()=='resolved'",
            login="demo",
        )
