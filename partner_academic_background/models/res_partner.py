# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _compute_count_academic_background(self):
        for partner in self:
            partner.count_academic_background = len(
                partner.academic_background_ids)

    academic_background_ids = fields.One2many(
        string='Academic background', inverse_name='partner_id',
        comodel_name='res.partner.academic.background')
    count_academic_background = fields.Integer(
        '# Academic background', compute='_compute_count_academic_background')

    def action_view_academic_background(self):
        context = self.env.context.copy()
        context.update({'default_partner_id': self.id})
        return {
            'name': _("Academic backgrounds"),
            'view_mode': 'tree,form',
            'res_model': 'res.partner.academic.background',
            'domain': [('id', 'in', self.academic_background_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }
