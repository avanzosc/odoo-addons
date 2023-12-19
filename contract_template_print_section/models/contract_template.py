# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ContractTemplate(models.Model):
    _inherit = 'contract.template'

    section_to_print_ids = fields.One2many(
        comodel_name='contract.template.line',
        inverse_name='contract_id', string='Sections to print',
        domain=[('display_type', '=', 'line_section')])

    def calculate_recalculate_to_print(self):
        for section in self.section_to_print_ids:
            lines = self.mapped('contract_line_ids').filtered(
                lambda x: x.sequence >= section.my_sequence and not
                x.display_type)
            if lines:
                lines.with_context(update_print=True).write(
                    {'print_section_lines':
                     section.print_section_lines})


class ContractTemplateLine(models.Model):
    _inherit = 'contract.template.line'

    print_section_lines = fields.Boolean(
        string='Print section lines', default=True)
    my_sequence = fields.Integer(string='My sequence', related='sequence')

    @api.model
    def create(self, vals):
        line = super(ContractTemplateLine, self).create(vals)
        line.contract_id.calculate_recalculate_to_print()
        return line

    @api.multi
    def write(self, vals):
        result = super(ContractTemplateLine, self).write(vals)
        lines = self.filtered(lambda x: x.display_type == 'line_section')
        if 'update_print'not in self.env.context and ('sequence' in vals):
            for line in self:
                line.contract_id.calculate_recalculate_to_print()
        if ('update_print'not in self.env.context and
           'print_section_lines' in vals):
            for line in lines:
                line.contract_id.calculate_recalculate_to_print()
        return result
