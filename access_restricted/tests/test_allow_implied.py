from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase, tagged


@tagged("at_install", "post_install")
class TestAllowImplied(TransactionCase):
    def test_base(self):
        demo_user = self.env.ref("base.user_demo")

        group_system = self.env.ref("base.group_system")
        group_private_addresses = self.env.ref("base.group_private_addresses")

        demo_user.write({"groups_id": [(3, group_private_addresses.id)]})
        group_private_addresses.write({"users": [(3, demo_user.id)]})
        self.assertFalse(
            self.env["res.users"]
            .sudo(demo_user.id)
            .has_group("base.group_private_addresses")
        )

        demo_user.write({"groups_id": [(4, group_system.id)]})

        test_config_settings = (
            self.env["test.config.settings"]
            .sudo(demo_user.id)
            .create({"group_private_addresses": True})
        )
        self.assertFalse(
            self.env["res.users"]
            .sudo(demo_user.id)
            .has_group("base.group_private_addresses")
        )

        # check that the field is readonly
        self.assertTrue(
            test_config_settings.fields_get()["group_private_addresses"]["readonly"]
        )
        # check that test group hasn't got appended to classified
        self.assertFalse(test_config_settings._get_classified_fields()["group"])

        group_allow = self.env.ref(
            "access_restricted.group_allow_add_implied_from_settings"
        )
        demo_user.write({"groups_id": [(4, group_allow.id)]})

        # check that now the field is not readonly
        self.assertFalse(
            test_config_settings.fields_get()["group_private_addresses"]["readonly"]
        )
        # check that now the group is in classified
        self.assertTrue(test_config_settings._get_classified_fields()["group"])

        self.assertFalse(
            self.env["res.users"]
            .sudo(demo_user.id)
            .has_group("base.group_private_addresses")
        )
        test_config_settings.sudo(demo_user.id).execute()
        self.assertTrue(
            self.env["res.users"]
            .sudo(demo_user.id)
            .has_group("base.group_private_addresses")
        )

    def test_assert_raises(self):

        demo_user = self.env.ref("base.user_demo")
        group_system = self.env.ref("base.group_system")
        group_private_addresses = self.env.ref("base.group_private_addresses")

        demo_user.write({"groups_id": [(3, group_private_addresses.id)]})
        group_private_addresses.write({"users": [(3, demo_user.id)]})
        self.assertFalse(
            self.env["res.users"]
            .sudo(demo_user.id)
            .has_group("base.group_private_addresses")
        )

        demo_user.write({"groups_id": [(4, group_system.id)]})
        self.assertFalse(
            self.env["res.users"]
            .sudo(demo_user.id)
            .has_group("base.group_private_addresses")
        )

        # check that there is no access to put test group into implied_ids anyways
        with self.assertRaises(AccessError):
            group_system.sudo(demo_user.id).write(
                {"implied_ids": [(4, group_private_addresses.id)]}
            )
