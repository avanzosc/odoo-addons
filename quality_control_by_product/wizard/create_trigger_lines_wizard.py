# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class CreateTriggerLinesWizard(models.TransientModel):

    _name = 'create.trigger.lines.wizard'

    trigger = fields.Many2one(comodel_name='qc.trigger', string='Trigger')

    @api.multi
    def create_trigger_lines(self):
        tests = self.env['qc.test'].browse(self.env.context.get('active_ids'))
        tests.create_trigger_line(self.trigger)
