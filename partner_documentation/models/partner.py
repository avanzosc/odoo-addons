# Copyright (c) 2017 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    document_lines = fields.One2many(
        comodel_name='partner.document',
        inverse_name='partner_id',
        string='Documents')
    document_count = fields.Integer(
        string='Documentation',
        compute='_compute_documentation_count')

    @api.multi
    def _compute_documentation_count(self):
        for partner in self:
            partner.document_count = len(
                partner.mapped('document_lines.document_attachment'))

    @api.multi
    def show_attachments(self):
        attachments = self.mapped('document_lines.document_attachment')
        if not attachments:
            return True
        result = self.env.ref('base.action_attachment').read()[0]
        result['domain'] = "[('id', 'in', {})]".format(attachments.ids)
        return result
