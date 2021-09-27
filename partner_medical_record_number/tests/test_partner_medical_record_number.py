# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestPartnerMedicalRecordNumber(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerMedicalRecordNumber, cls).setUpClass()
        cls.contact_obj = cls.env['res.partner']
        cls.partner1 = cls.contact_obj.create({
            'name': 'Parent1',
        })
        cls.partner2 = cls.contact_obj.create({
            'name': 'Parent2',
        })

    def test_partner_medical_record_number(self):
        self.assertEqual(self.partner1.last_adult_number, 0)
        self.assertEqual(self.partner1.last_child_number, 0)
        self.partner1.adult_medical_record = 9991
        self.partner2.adult_medical_record = 9999
        self.assertEqual(self.partner1.last_adult_number, 9999)
        self.partner1.child_medical_record = 2221
        self.partner2.child_medical_record = 2222
        self.assertEqual(self.partner1.last_child_number, 2222)
