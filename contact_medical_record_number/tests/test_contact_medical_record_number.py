# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestContactMedicalRecordNumber(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestContactMedicalRecordNumber, cls).setUpClass()
        cls.contact_obj = cls.env['res.partner']
        cls.parent1 = cls.contact_obj.create({
            'name': 'Parent1',
            'company_type': 'company',
        })
        cls.parent2 = cls.contact_obj.create({
            'name': 'Parent2',
            'company_type': 'company',
        })
        cls.partner1 = cls.contact_obj.create({
            'name': 'Partner1',
            'company_type': 'person',
            'parent_id': cls.parent1.id,
        })
        cls.partner2 = cls.contact_obj.create({
            'name': 'Partner2',
            'company_type': 'person',
            'parent_id': cls.parent1.id,
        })

    def test_contact_medical_record_number(self):
        self.assertEqual(self.parent1.last_parent_number, 0)
        self.assertEqual(self.partner1.last_partner_number, 0)
        self.parent1.parent_medical_record = 9991
        self.parent2.parent_medical_record = 9999
        self.assertEqual(self.parent1.last_parent_number, 9999)
        self.partner1.partner_medical_record = 2221
        self.partner2.partner_medical_record = 2222
        self.assertEqual(self.partner1.last_partner_number, 2222)
        self.assertEqual(self.partner1.parent_medical_record, 9991)
