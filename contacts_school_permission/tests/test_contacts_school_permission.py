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
