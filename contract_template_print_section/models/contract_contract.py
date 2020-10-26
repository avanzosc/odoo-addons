# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    section_to_print_ids = fields.One2many(
        comodel_name='contract.line',
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

    @api.onchange('contract_template_id')
    def _onchange_contract_template_id(self):
        contract_template_id = self.contract_template_id
        if not contract_template_id:
            return
        for field_name, field in contract_template_id._fields.items():
            if field.name == 'contract_line_ids':
                lines = self._convert_contract_lines(contract_template_id)
                self.contract_line_ids += lines
            elif not any(
                (
                    field.compute,
                    field.related,
                    field.automatic,
                    field.readonly,
                    field.company_dependent,
                    field.name in self.NO_SYNC,
                )
            ):
                if (field_name and field_name != 'section_to_print_ids' and
                        self.contract_template_id[field_name]):
                    self[field_name] = self.contract_template_id[field_name]
