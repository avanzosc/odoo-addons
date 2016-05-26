# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _partner_inspections_count(self):
        inspection_obj = self.env['qc.inspection']
        for partner in self:
            partner.inspections_count = 0
            cond = [('object_id', '=', 'res.partner,' + str(partner.id))]
            inspections = inspection_obj.search(cond)
            partner.inspections_count = len(inspections)

    inspections_count = fields.Integer(
        string='# Inspection', compute=_partner_inspections_count)

    @api.multi
    def inspections_from_partner(self):
        inspection_obj = self.env['qc.inspection']
        self.ensure_one()
        cond = [('object_id', '=', 'res.partner,' + str(self.id))]
        inspections = inspection_obj.search(cond)
        return {'name': _('Inspections'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'qc.inspection',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', inspections.ids)]}
