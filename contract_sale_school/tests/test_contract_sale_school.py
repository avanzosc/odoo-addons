# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase
from odoo import fields


class TestContractSaleSchool(TransactionCase):

    def setUp(self):
        super(TestContractSaleSchool, self).setUp()
        self.partner_model = self.env['res.partner']
        self.product_model = self.env['product.product']
        self.sale_model = self.env['sale.order']
        self.payer_model = self.env['sale.order.line.payer']
        self.education_plan_model = self.env['education.plan']
        self.education_level_model = self.env['education.level']
        self.education_course_model = self.env['education.course']
        self.academic_year_model = self.env['education.academic_year']
        self.partner = self.partner_model.search([], limit=1)
        student_vals = {
            'name': 'Student for test contract_sale_school',
            'educational_category': 'student'}
        self.student = self.partner_model.create(student_vals)
        school_vals = {
            'name': 'School for test contract_sale_school',
            'educational_category': 'school'}
        self.school = self.partner_model.create(school_vals)
        education_plan_vals = {
            'description': 'Education plan for test sale_crm_school',
            'education_code': 'code-1'}
        self.education_plan = self.education_plan_model.create(
            education_plan_vals)
        education_level_vals = {
            'education_code': 'level-1',
            'description': 'Level for test sale_crm_school',
            'short_description': 'L-1',
            'plan_id': self.education_plan.id}
        self.education_level = self.education_level_model.create(
            education_level_vals)
        education_course_vals = {
            'education_code': 'C1',
            'level_id': self.education_level.id,
            'description': 'Course 1'}
        self.education_course = self.education_course_model.create(
            education_course_vals)
        date_from = "{}-01-01".format(
            fields.Date.from_string(fields.Date.today()).year)
        date_from = fields.Date.from_string(date_from)
        date_to = "{}-12-31".format(
            int(fields.Date.from_string(fields.Date.today()).year)
            + 1)
        date_to = fields.Date.from_string(date_to)
        academic_year_vals = {
            'name': 'BBBBB2020',
            'date_start': date_from,
            'date_end': date_to}
        self.academic_year = self.academic_year_model.create(
            academic_year_vals)
        cond = [('sale_ok', '=', True)]
        self.product1 = self.product_model.search(cond, limit=1)
        cond = [('sale_ok', '=', True),
                ('id', '>', self.product1.id)]
        self.product2 = self.product_model.search(cond, limit=1)
        sale_vals = {
            'partner_id': self.partner.id,
            'child_id': self.student.id,
            'school_id': self.school.id,
            'course_id': self.education_course.id,
            'academic_year_id': self.academic_year.id}
        self.sale = self.env['sale.order'].create(sale_vals)

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
        cond = [('sale_id', '=', self.sale.id)]
        self.assertEqual(res.get('domain'), cond)
        self.assertEqual(self.sale.contracts_count, 2)
        contract = self.sale.analytic_account_ids.filtered(
            lambda c: c.partner_id.id == 2)
        self.assertEqual(len(contract.recurring_invoice_line_ids), 1)
        for line in contract.recurring_invoice_line_ids:
            self.assertEqual(line.payment_percentage, 75.0)
        contract = self.sale.analytic_account_ids.filtered(
            lambda c: c.partner_id.id == 3)
        self.assertEqual(len(contract.recurring_invoice_line_ids), 1)
        for line in contract.recurring_invoice_line_ids:
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
        contract = self.sale.analytic_account_ids.filtered(
            lambda c: c.partner_id.id == 4)
        self.assertEqual(len(contract.recurring_invoice_line_ids), 2)
        for line in contract.recurring_invoice_line_ids:
            self.assertEqual(line.payment_percentage, 100.0)
