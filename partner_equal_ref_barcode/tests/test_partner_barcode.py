# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestPartnerBarcode(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerBarcode, cls).setUpClass()
        cls.company = cls.env.ref('base.main_company')
        cls.partner_obj = cls.env['res.partner']
        cls.p1 = cls.partner_obj.create({
            'name': 'p1',
        })
        cls.p2 = cls.partner_obj.create({
            'name': 'p2',
        })

    def test_check_barcode_company(self):
        # Test can create/modify partners with same barcode
        self.company.partner_barcode_unique = 'none'
        self.p1.barcode = 'equal_barcode'
        self.p2.barcode = 'equal_barcode'
        self.assertEqual(self.p1.barcode, self.p2.barcode)
        # Here there shouldn't be any problem
        self.partner_obj.create({
            'name': 'other',
            'barcode': 'equal_barcode',
        })
        self.p2.barcode = False
        with self.assertRaises(ValidationError):
            self.company.partner_barcode_unique = 'all'

    def test_check_barcode(self):
        self.p1.barcode = 'equal_barcode'
        # Test can't create/modify partner with same barcode
        self.company.partner_barcode_unique = 'all'
        with self.assertRaises(ValidationError):
            self.p2.barcode = 'equal_barcode'
        with self.assertRaises(ValidationError):
            self.partner_obj.create({
                'name': 'other',
                'barcode': 'equal_barcode',
            })
        # Test can't create/modify companies with same barcode
        self.company.partner_barcode_unique = 'companies'
        self.p2.barcode = 'equal_barcode'
        self.assertEqual(self.p1.barcode, self.p2.barcode)
        self.p2.barcode = False
        self.p1.is_company = True
        self.p2.is_company = True
        with self.assertRaises(ValidationError):
            self.p2.barcode = 'equal_barcode'
        with self.assertRaises(ValidationError):
            self.partner_obj.create({
                'is_company': True,
                'name': 'other',
                'barcode': 'equal_barcode',
            })
        # Here there shouldn't be any problem
        self.partner_obj.create({
            'is_company': False,
            'name': 'other',
            'barcode': 'equal_barcode',
        })

    def test_onchange_ref_barcode(self):
        self.p1.barcode = 'barcode_ref'
        self.p1.onchange_barcode()
        self.assertEqual(self.p1.barcode, self.p1.ref)
        self.p2.ref = 'ref_barcode'
        self.p2.onchange_ref()
        self.assertEqual(self.p2.ref, self.p2.barcode)
