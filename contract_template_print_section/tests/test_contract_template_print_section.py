# Copyright (c) 2020 Alfredo de la fuente - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestContractTemplatePrintSection(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestContractTemplatePrintSection, cls).setUpClass()
        cls.partner_model = cls.env['res.partner']
        cls.invoice_model = cls.env['account.invoice']
        cls.partner = cls.env.ref('base.res_partner_12')
        cls.contract_model = cls.env['contract.contract']
        cls.product = cls.env.ref('product.consu_delivery_01')
        cls.product2 = cls.env.ref('product.consu_delivery_02')
        template_vals = {
            'name': 'Sale for test sale_stock_analytic',
            'partner_id': cls.partner.id}
        template_line1_vals = {
            'product_id': cls.product.id,
            'name': 'Section 1',
            'display_type': 'line_section',
            'sequence': 10}
        template_line2_vals = {
            'product_id': cls.product.id,
            'name': cls.product.name,
            'product_uom_qty': 1,
            'product_uom_id': cls.product.uom_id.id,
            'price_unit': 100,
            'sequence': 20}
        template_line3_vals = {
            'product_id': cls.product.id,
            'name': 'Section 2',
            'display_type': 'line_section',
            'sequence': 30}
        template_line4_vals = {
            'product_id': cls.product2.id,
            'name': cls.product2.name,
            'product_uom_qty': 5,
            'product_uom_id': cls.product2.uom_id.id,
            'price_unit': 25,
            'sequence': 40}
        template_vals['contract_line_ids'] = [
            (0, 0, template_line1_vals), (0, 0, template_line2_vals),
            (0, 0, template_line3_vals), (0, 0, template_line4_vals)]
        cls.contract_template = cls.env['contract.template'].create(
            template_vals)

    def test_contract_template_print_section(self):
        vals = {'name': self.partner.name,
                'partner_id': self.partner.id,
                'contract_template_id': self.contract_template.id}
        contract = self.contract_model.create(vals)
        contract._onchange_contract_template_id()
        lines = contract.contract_line_ids.filtered(
            lambda x: x.print_section_lines)
        self.assertEqual(len(lines), 4)
        contract.section_to_print_ids[0].print_section_lines = False
        lines = contract.contract_line_ids.filtered(
            lambda x: x.print_section_lines)
        self.assertEqual(len(lines), 2)
        contract.section_to_print_ids[0].print_section_lines = True
        lines = contract.contract_line_ids.filtered(
            lambda x: x.display_type != 'line_section')
        lines[0].print_section_lines = False
        lines = contract.contract_line_ids.filtered(
            lambda x: x.print_section_lines)
        self.assertEqual(len(lines), 3)
        lines[0].print_section_lines = True
        lines = contract.contract_line_ids.filtered(
            lambda x: x.print_section_lines)
        self.assertEqual(len(lines), 4)
        contract.recurring_create_invoice()
        cond = [('type', '=', 'out_invoice'),
                ('partner_id', '=', self.partner.id),
                ('state', '=', 'draft')]
        invoice = self.invoice_model.search(cond)
        lines = invoice.invoice_line_ids.filtered(
            lambda x: x.print_section_lines)
        self.assertEqual(len(lines), 4)
        invoice.section_to_print_ids[0].print_section_lines = False
        lines = invoice.invoice_line_ids.filtered(
            lambda x: x.print_section_lines)
        self.assertEqual(len(lines), 2)
        invoice.section_to_print_ids[0].print_section_lines = True
        lines = invoice.invoice_line_ids.filtered(
            lambda x: x.display_type != 'line_section')
        lines[0].print_section_lines = False
        lines = invoice.invoice_line_ids.filtered(
            lambda x: x.print_section_lines)
        self.assertEqual(len(lines), 3)
