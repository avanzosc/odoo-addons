from odoo.tests import common

from odoo.addons.access_restricted.tests.test_fields_view_get import (
    TestFieldsViewGet as TestFieldsViewGetBase,
)


@common.tagged("post_install", "-at_install")
class TestFieldsViewGet(TestFieldsViewGetBase):
    def test_access_settings_menu(self):
        admin = self.env.ref("base.user_root")
        demo = self.env.ref("base.user_demo")

        # demo doesn't have admin rights, but has "Show Settings Menu"
        self.clear_access(demo)
        self.add_access(demo, "access_settings_menu.group_show_settings_menu")
        self.view_form_all(demo)
        self.view_form_mix(admin, demo)
        self.clear_config()
        self.view_form_mix(demo, admin)
