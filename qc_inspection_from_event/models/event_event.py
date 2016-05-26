# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.multi
    def _event_inspections_count(self):
        inspection_obj = self.env['qc.inspection']
        for event in self:
            event.inspections_count = 0
            cond = [('object_id', '=', 'event.event,' + str(event.id))]
            inspections = inspection_obj.search(cond)
            event.inspections_count = len(inspections)

    inspections_count = fields.Integer(
        string='# Inspection', compute=_event_inspections_count)

    @api.multi
    def inspections_from_event(self):
        inspection_obj = self.env['qc.inspection']
        self.ensure_one()
        cond = [('object_id', '=', 'event.event,' + str(self.id))]
        inspections = inspection_obj.search(cond)
        return {'name': _('Inspections'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'qc.inspection',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', inspections.ids)]}
