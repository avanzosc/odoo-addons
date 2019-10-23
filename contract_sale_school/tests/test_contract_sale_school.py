# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
from odoo import exceptions, fields


@common.at_install(False)
@common.post_install(True)
class TestContractSaleSchool(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestContractSaleSchool, cls).setUpClass()
        cls.partner_model = cls.env['res.partner']
        cls.product_model = cls.env['product.product']
        cls.sale_model = cls.env['sale.order']
        cls.payer_model = cls.env['sale.order.line.payer']
        cls.education_plan_model = cls.env['education.plan']
        cls.education_level_model = cls.env['education.level']
        cls.education_course_model = cls.env['education.course']
        cls.academic_year_model = cls.env['education.academic_year']
        cls.partner = cls.partner_model.search([], limit=1)
        student_vals = {
            'name': 'Student for test contract_sale_school',
            'educational_category': 'student'}
        cls.student = cls.partner_model.create(student_vals)
        school_vals = {
            'name': 'School for test contract_sale_school',
            'educational_category': 'school'}
        cls.school = cls.partner_model.create(school_vals)
        education_plan_vals = {
            'description': 'Education plan for test sale_crm_school',
            'education_code': 'PLAN'}
        cls.education_plan = cls.education_plan_model.create(
            education_plan_vals)
        education_level_vals = {
            'education_code': 'LVL1',
            'description': 'Level for test sale_crm_school',
            'short_description': 'L-1',
            'plan_id': cls.education_plan.id}
        cls.education_level = cls.education_level_model.create(
            education_level_vals)
        education_course_vals = {
            'education_code': 'CRS1',
            'level_id': cls.education_level.id,
            'description': 'Course 1'}
        cls.education_course = cls.education_course_model.create(
            education_course_vals)
        today = fields.Date.today()
        date_from = today.replace(month=1, day=1)
        date_to = today.replace(year=today.year + 1, month=12, day=31)
        academic_year_vals = {
            'name': '{}-{}'.format(date_to.year, date_from.year),
            'date_start': date_from,
            'date_end': date_to,
        }
        cls.academic_year = cls.academic_year_model.create(
            academic_year_vals)
        cond = [('sale_ok', '=', True)]
        cls.product1 = cls.product_model.search(cond, limit=1)
        cond = [('sale_ok', '=', True),
                ('id', '>', cls.product1.id)]
        cls.product2 = cls.product_model.search(cond, limit=1)
        sale_vals = {
            'partner_id': cls.partner.id,
            'child_id': cls.student.id,
            'school_id': cls.school.id,
            'course_id': cls.education_course.id,
            'academic_year_id': cls.academic_year.id}
        cls.sale = cls.env['sale.order'].create(sale_vals)

    def test_contract_sale_school_recurring(self):
        self.product2.write({
            'recurrent_punctual': 'recurrent',
            'month_start':
            self.browse_ref('base_month.base_month_november').id,
            'end_month': self.browse_ref('base_month.base_month_january').id})
        sale_line_vals = {
            'product_id': self.product2.id,
            'name': self.product2.name,
            'originator_id': 1,
            'product_uom': self.product2.uom_id.id,
            'price_unit': self.product2.list_price}
        self.sale.order_line = [(0, 0, sale_line_vals)]
        with self.assertRaises(exceptions.Warning):
            self.sale.action_confirm()
        payer_vals = {
            'line_id': self.sale.order_line[0].id,
            'payer_id': 2,
            'pay_percentage': 75.0}
        self.payer_model.create(payer_vals)
        payer_vals = {
            'line_id': self.sale.order_line[0].id,
            'payer_id': 3,
            'pay_percentage': 25.0}
        self.payer_model.create(payer_vals)
        self.sale.action_confirm()
        res = self.sale.action_view_contracts()
        cond = ('sale_id', 'in', self.sale.ids)
        self.assertIn(cond, res.get('domain'))
        self.assertEqual(self.sale.contracts_count, 2)
        contract = self.sale.contract_ids.filtered(
            lambda c: c.partner_id.id == 2)
        self.assertEqual(len(contract.contract_line_ids), 1)
        for line in contract.contract_line_ids:
            self.assertEqual(line.payment_percentage, 75.0)
        contract = self.sale.contract_ids.filtered(
            lambda c: c.partner_id.id == 3)
        self.assertEqual(len(contract.contract_line_ids), 1)
        for line in contract.contract_line_ids:
            self.assertEqual(line.payment_percentage, 25.0)

    def test_contract_sale_school_punctual(self):
        self.product2.write({
            'recurrent_punctual': 'punctual',
            'punctual_month_ids':
            [(6, 0, [self.browse_ref('base_month.base_month_january').id,
                     self.browse_ref('base_month.base_month_february').id])]})
        sale_line_vals = {
            'product_id': self.product2.id,
            'name': self.product2.name,
            'originator_id': 1,
            'product_uom': self.product2.uom_id.id,
            'price_unit': self.product2.list_price}
        self.sale.order_line = [(0, 0, sale_line_vals)]
        payer_vals = {
            'line_id': self.sale.order_line[0].id,
            'payer_id': 4,
            'pay_percentage': 100.0}
        self.payer_model.create(payer_vals)
        self.sale.action_confirm()
        self.assertEqual(self.sale.contracts_count, 1)
        contract = self.sale.contract_ids.filtered(
            lambda c: c.partner_id.id == 4)
        self.assertEqual(len(contract.contract_line_ids), 2)
        for line in contract.contract_line_ids:
            self.assertEqual(line.payment_percentage, 100.0)
