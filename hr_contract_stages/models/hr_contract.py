# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    @api.multi
    def _default_stage_id(self):
        stages = self.env['hr.contract.stage'].search([])
        return stages and stages[0] or []

    contract_stage_id = fields.Many2one(
        comodel_name='hr.contract.stage', string='Stage',
        default=_default_stage_id)
