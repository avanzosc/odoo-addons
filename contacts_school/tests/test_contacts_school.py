# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.exceptions import ValidationError
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestContactsSchool(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestContactsSchool, cls).setUpClass()
        cls.family_sequence = cls.env.ref(
            'contacts_school.seq_res_partner_family')
        cls.partner_model = cls.env['res.partner']
        cls.family_model = cls.env['res.partner.family']
        cls.user_model = cls.env['res.users']
        cls.employee_model = cls.env['hr.employee']
        cls.family = cls.partner_model.create({
            'name': 'Test Family',
            'educational_category': 'family',
            'is_company': True,
        })
        cls.relative = cls.partner_model.create({
            'name': 'Test Relative',
            'educational_category': 'otherrelative',
            'is_company': False,
            'parent_id': cls.family.id,
            'bank_ids': [
                (0, 0, {
                    'acc_number': '0123456789',
                }),
                (0, 0, {
                    'acc_number': '9876543210',
                })]
        })
        cls.student = cls.partner_model.create({
            'name': 'Test Student',
            'educational_category': 'student',
            'is_company': False,
            'parent_id': cls.family.id,
        })

    def test_family_code(self):
        self.assertTrue(self.family.family)
        code = self._get_next_code()
        new_family = self.partner_model.create({
            'name': 'New Test Family',
            'educational_category': 'family',
        })
        self.assertEquals(new_family.family, code)

    def test_family_relation(self):
        self.assertFalse(self.relative.is_company)
        self.assertFalse(self.family.family_progenitor_ids)
        self.assertFalse(self.student.student_progenitor_ids)
        relation = self.family_model.create({
            'child2_id': self.student.id,
            'responsible_id': self.relative.id,
            'family_id': self.family.id,
            'relation': 'progenitor',
        })
        self.family.invalidate_cache()
        self.assertTrue(self.family.family_progenitor_ids)
        self.assertTrue(self.student.student_progenitor_ids)
        name = self.family.with_context(
            hide_progenitors=False).name_get()[0][1]
        family_progenitors = ', '.join(self.family.mapped(
            'family_progenitor_ids.name'))
        family_name = "{} [{}]".format(self.family.name, family_progenitors)
        self.assertEquals(name, family_name)
        self.assertFalse(self.relative.is_company)
        self.assertIn(self.relative, self.family.family_progenitor_ids)
        self.assertIn(self.relative, self.student.student_progenitor_ids)
        relation.write({
            'payer': True,
        })
        self.assertTrue(self.relative.is_company)
        with self.assertRaises(ValidationError):
            relation.write({
                'payment_percentage': 105.0,
            })
        with self.assertRaises(ValidationError):
            relation.write({
                'payment_percentage': 0.0,
            })
        self.assertNotEquals(
            self.relative.bank_ids[:1], self.relative.bank_ids[1:])
        relation.onchange_responsible_id()
        self.assertEquals(relation.bank_id, self.relative.bank_ids[:1])
        self.relative.bank_ids[1:].write({
            'use_default': True,
        })
        relation.onchange_responsible_id()
        self.assertEquals(relation.bank_id, self.relative.bank_ids[1:])

    def test_student_family_relation(self):
        with self.assertRaises(ValidationError):
            self.student.write({
                'child2_ids': [(0, 0, {
                    'responsible_id': self.relative.id,
                    'family_id': self.family.id,
                    'payer': True,
                    'payment_percentage': 95.0,
                })],
            })

    def test_partner_employee(self):
        user = self.user_model.create({
            'name': 'Test User',
            'login': 'test_user',
            'email': 'mymail@test.com',
        })
        self.assertFalse(user.partner_id.employee)
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'user_id': user.id,
        })
        self.assertTrue(user.partner_id.employee)
        self.assertEquals(user.partner_id.employee_id, employee)

    def _get_next_code(self):
        return self.family_sequence.get_next_char(
            self.family_sequence.number_next_actual)
