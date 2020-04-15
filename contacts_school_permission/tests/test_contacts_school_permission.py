# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.addons.contacts_school.tests.test_contacts_school import \
    TestContactsSchool


@common.at_install(False)
@common.post_install(True)
class TestContactsSchoolPermission(TestContactsSchool):

    @classmethod
    def setUpClass(cls):
        super(TestContactsSchoolPermission, cls).setUpClass()
        cls.permission_model = cls.env['res.partner.permission']
        cls.permission_wiz_model = cls.env['res.partner.permission.create']
        cls.permission_type = cls.env['res.partner.permission.type'].create({
            'name': 'Test Type',
        })

    def test_family_code(self):
        """Don't repeat this test."""
        pass

    def test_family_relation(self):
        super(TestContactsSchoolPermission, self).test_family_relation()
        permission = self.permission_model.create({
            'partner_id': self.student.id,
            'type_id': self.permission_type.id,
        })
        self.assertIn(self.relative, permission.allowed_signer_ids)

    def test_student_family_relation(self):
        """Don't repeat this test."""
        pass

    def test_partner_employee(self):
        """Don't repeat this test."""
        pass

    def test_permission_sign(self):
        permission = self.permission_model.create({
            'partner_id': self.student.id,
            'type_id': self.permission_type.id,
        })
        self.assertEquals(permission.state, 'pending')
        self.assertFalse(permission.signer_id)
        permission.button_sign()
        self.assertEquals(permission.state, 'yes')
        self.assertEquals(permission.signer_id, self.env.user.partner_id)

    def test_permission_deny(self):
        permission = self.permission_model.create({
            'partner_id': self.student.id,
            'type_id': self.permission_type.id,
        })
        self.assertEquals(permission.state, 'pending')
        self.assertFalse(permission.signer_id)
        permission.button_deny()
        self.assertEquals(permission.state, 'no')
        self.assertEquals(permission.signer_id, self.env.user.partner_id)

    def test_permission_wizard(self):
        partners = self.student | self.family | self.relative
        self.assertFalse(partners.mapped('permission_ids').filtered(
            lambda p: p.type_id == self.permission_type))
        wiz = self.permission_wiz_model.with_context(
            active_model=partners._name,
            active_ids=partners.ids).create({
                'type_id': self.permission_type.id,
            })
        self.assertNotEquals(wiz.student_ids, partners)
        self.assertEquals(wiz.student_ids, partners.filtered(
            lambda p: p.educational_category in ['student', 'otherchild']))
        wiz.create_permissions()
        self.assertTrue(partners.mapped('permission_ids').filtered(
            lambda p: p.type_id == self.permission_type))
