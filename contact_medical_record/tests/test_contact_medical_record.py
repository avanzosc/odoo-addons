# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestContactMedicalRecord(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestContactMedicalRecord, cls).setUpClass()
        cls.contact_obj = cls.env['res.partner']
        cls.parent = cls.contact_obj.create({
            'name': 'Parent',
            'company_type': 'company',
            'partner_medical_record_ids': [
                (0, 0, {
                    'number': 1234,
                }),
                (0, 0, {
                    'number': 2345,
                }),
            ],
        })
        cls.partner = cls.contact_obj.create({
            'name': 'Partner',
            'company_type': 'person',
            'parent_id': cls.parent.id,
            'partner_medical_record_ids': [
                (0, 0, {
                    'number': 1237,
                }),
                (0, 0, {
                    'number': 2349,
                }),
            ],
        })

    def test_contact_medical_record(self):
        action_parent = self.parent.action_view_medical_record()
        self.assertEqual(len(action_parent['domain'][0][2]), 1)
        action_partner = self.partner.action_view_medical_record()
        self.assertEqual(len(action_partner['domain'][0][2]), 2)
