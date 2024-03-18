from odoo.tests.common import TransactionCase, tagged

IR_CONFIG_NAME = "access_restricted.fields_view_get_uid"


@tagged("post_install", "-at_install")
class TestFieldsViewGet(TransactionCase):
    def clear_config(self):
        self.env["ir.config_parameter"].search([("key", "=", IR_CONFIG_NAME)]).unlink()

    def clear_access(self, user):
        user.write(
            {
                "groups_id": [
                    (3, self.env.ref("base.group_erp_manager").id, 0),
                    (3, self.env.ref("base.group_system").id, 0),
                ]
            }
        )

    def add_access(self, user, group_xmlid):
        user.write({"groups_id": [(4, self.env.ref(group_xmlid).id, 0)]})

    def _view_form(self, user, view_xmlid):
        view_id = self.env.ref(view_xmlid).id
        # context = {'lang': "en_US", 'tz': "Europe/Brussels", 'uid': user.id}
        self.env["res.users"].sudo(user.id).fields_view_get(view_id=view_id)

    def view_preference_form(self, user):
        self._view_form(user, "base.view_users_form_simple_modif")

    def view_user_form(self, user):
        self._view_form(user, "base.view_users_form")

    def view_form_all(self, user):
        self.view_preference_form(user)
        self.clear_config()

        self.view_user_form(user)
        self.clear_config()

    def view_form_mix(self, user1, user2):
        self.view_preference_form(user1)
        self.view_user_form(user2)

        self.view_preference_form(user1)
        self.view_preference_form(user2)

        self.view_form_all(user1)
        self.view_user_form(user2)

    def test_base(self):
        admin = self.env.ref("base.user_root")
        demo = self.env.ref("base.user_demo")

        # test for admin
        self.view_form_all(admin)

        # demo doesn't have admin rights
        self.clear_access(demo)
        self.view_preference_form(demo)

        # demo has "Access Rights"
        self.add_access(demo, "base.group_erp_manager")
        self.view_form_all(demo)

        # demo has "Settings"
        self.add_access(demo, "base.group_system")
        self.view_form_all(demo)

        self.view_form_mix(admin, demo)
