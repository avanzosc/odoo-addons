# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ContractLine(models.Model):
    _inherit = 'contract.line'

    print_section_lines = fields.Boolean(
        string='Print section lines', default=True)
    my_sequence = fields.Integer(string='My sequence', related='sequence')

    @api.model
    def create(self, vals):
        line = super(ContractLine, self).create(vals)
        line.contract_id.calculate_recalculate_to_print()
        return line

    @api.multi
    def write(self, vals):
        result = super(ContractLine, self).write(vals)
        lines = self.filtered(lambda x: x.display_type == 'line_section')
        if 'update_print'not in self.env.context and ('sequence' in vals):
            for line in self:
                line.contract_id.calculate_recalculate_to_print()
        if ('update_print'not in self.env.context and
           'print_section_lines' in vals):
            for line in lines:
                line.contract_id.calculate_recalculate_to_print()
        return result
