# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    contract_line_id = fields.Many2one(
        string='Contract line', comodel_name='contract.line')
    contract_id = fields.Many2one(
        string='Contract', comodel_name='contract.contract',
        related='contract_line_id.contract_id', store=True)

    def _synchronize_so_line_values(self, so_line):
        reg_vals = super(EventRegistration,
                         self)._synchronize_so_line_values(so_line)
        if so_line:
            reg_vals.update({
                "contract_line_id": so_line.contract_line_id.id,
            })
        return reg_vals
