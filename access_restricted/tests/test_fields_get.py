from odoo.tests.common import TransactionCase, tagged

from odoo.addons.base.models.res_users import name_selection_groups


@tagged("at_install", "post_install")
class TestFieldsGet(TransactionCase):
    def test_base(self):
        demo_user = self.env.ref("base.user_demo")
        group_erp_manager = self.env.ref("base.group_erp_manager")
        group_system = self.env.ref("base.group_system")

        demo_user.write({"groups_id": [(3, group_system.id)]})
        group_system.write({"users": [(3, demo_user.id)]})
        demo_user.write({"groups_id": [(4, group_erp_manager.id)]})

        view_users_form = self.env.ref("base.view_users_form")
        res = (
            self.env["res.users"]
            .sudo(demo_user)
            .with_context({"uid": demo_user.id})
            .load_views([[view_users_form.id, "form"]])
        )

        sel_groups = name_selection_groups([group_erp_manager.id])
        res = self.env["res.users"].sudo(demo_user).fields_get()
        self.assertTrue(res.get(sel_groups))

        demo_user.write({"groups_id": [(4, group_system.id)]})

        sel_groups = name_selection_groups([group_erp_manager.id, group_system.id])
        res = self.env["res.users"].sudo(demo_user).fields_get()
        self.assertTrue(res.get(sel_groups))
