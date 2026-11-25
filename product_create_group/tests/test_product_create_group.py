# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import AccessError
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestProductCreateGroup(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = cls.env.ref("product_create_group.group_create_product_tmpl")
        cls.access = cls.env.ref("product_create_group.access_create_product_tmpl")
        cls.product_tmpl_model = cls.env["ir.model"].search(
            [("model", "=", "product.template")], limit=1
        )
        cls.base_user = cls.env.ref("base.group_user")
        cls.product_manager = cls.env.ref("product.group_product_manager")

    def test_01_group_exists(self):
        self.assertTrue(self.group, "Group should exist after install")
        self.assertEqual(self.group.name, "Create Product Tmpl")

    def test_02_acl_exists_and_grants_create_unlink(self):
        self.assertTrue(self.access)
        self.assertEqual(self.access.model_id, self.product_tmpl_model)
        self.assertEqual(self.access.group_id, self.group)
        self.assertTrue(self.access.perm_read)
        self.assertTrue(self.access.perm_write)
        self.assertTrue(
            self.access.perm_create,
            "Our ACL must grant create on product.template",
        )
        self.assertTrue(
            self.access.perm_unlink,
            "Our ACL must grant unlink on product.template",
        )

    def test_03_other_acls_lost_create_unlink(self):
        """post_init_hook and init() must clear perm_create / perm_unlink
        on every other ACL targeting product.template."""
        other_acls = self.env["ir.model.access"].search(
            [
                ("model_id", "=", self.product_tmpl_model.id),
                ("id", "!=", self.access.id),
            ]
        )
        self.assertTrue(other_acls, "There should be other ACLs to compare")
        offenders = other_acls.filtered(lambda a: a.perm_create or a.perm_unlink)
        self.assertFalse(
            offenders,
            "These ACLs still grant create/unlink on product.template "
            f"after install: {offenders.mapped('name')}",
        )

    def test_04_product_manager_alone_cannot_create_template(self):
        """A user that has the standard Odoo 'Product Creation' group but NOT
        our new group must no longer be able to create a product.template:
        our post_init_hook stripped perm_create from that ACL."""
        user = self.env["res.users"].create(
            {
                "name": "PCG Test - product manager only",
                "login": "pcg_test_pm_only",
                "groups_id": [(6, 0, [self.base_user.id, self.product_manager.id])],
            }
        )
        env_user = self.env(user=user)
        with self.assertRaises(AccessError) as ctx:
            env_user["product.template"].create({"name": "Forbidden tmpl"})
        # Make sure the denial is about product.template, not a downstream model
        self.assertIn("product.template", str(ctx.exception))

    def test_05_plain_user_cannot_create_template(self):
        user = self.env["res.users"].create(
            {
                "name": "PCG Test - plain",
                "login": "pcg_test_plain",
                "groups_id": [(6, 0, [self.base_user.id])],
            }
        )
        env_user = self.env(user=user)
        with self.assertRaises(AccessError):
            env_user["product.template"].create({"name": "No way"})

    def test_07_init_works_when_our_ref_is_missing(self):
        """Simulates the first-install path: init() must still strip create
        and unlink on existing ACLs even when our own xmlid does not yet
        resolve (which is what happens before the XML data is loaded on a
        fresh install)."""
        AccessModel = self.env["ir.model.access"]
        # Build a fresh ACL on product.template with create/unlink and no
        # link to our module to make sure it gets stripped.
        sentinel = AccessModel.create(
            {
                "name": "pcg sentinel",
                "model_id": self.product_tmpl_model.id,
                "group_id": self.env.ref("base.group_user").id,
                "perm_read": True,
                "perm_write": True,
                "perm_create": True,
                "perm_unlink": True,
            }
        )
        # Remove our xmlid so env.ref raises ValueError (like first install).
        self.env["ir.model.data"].search(
            [
                ("module", "=", "product_create_group"),
                ("name", "=", "access_create_product_tmpl"),
            ]
        ).unlink()
        with self.assertRaises(ValueError):
            self.env.ref("product_create_group.access_create_product_tmpl")
        AccessModel.init()
        sentinel.invalidate_recordset()
        self.assertFalse(sentinel.perm_create)
        self.assertFalse(sentinel.perm_unlink)

    def test_06_user_with_group_can_create_and_unlink(self):
        """Realistic scenario: a user assigned the new group on top of the
        standard 'Product Creation' role must be able to create AND unlink
        product templates end-to-end (including the auto-created variants)."""
        user = self.env["res.users"].create(
            {
                "name": "PCG Test - with group",
                "login": "pcg_test_withgroup",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.base_user.id,
                            self.product_manager.id,
                            self.group.id,
                        ],
                    )
                ],
            }
        )
        env_user = self.env(user=user)
        product = env_user["product.template"].create({"name": "Allowed product"})
        self.assertTrue(product.exists())
        product.unlink()
        self.assertFalse(product.exists())
