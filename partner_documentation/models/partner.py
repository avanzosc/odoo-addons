# Copyright (c) 2017 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _compute_documentation_count(self):
        doc_obj = self.env['partner.document']
        for partner in self:
            partner.document_count = doc_obj.search_count(
                [('partner_id', '=', partner.id),
                 ('document_attachment', '!=', False)])

    document_lines = fields.One2many(
        comodel_name="partner.document",
        inverse_name='partner_id', string='Documents')
    document_count = fields.Integer("Documentation",
                                    compute='_compute_documentation_count')

    @api.multi
    def show_attachments(self):
        attachmen_lst = self.document_lines.filtered(
            lambda x: x.document_attachment)
        search_view = self.env.ref('base.view_attachment_search')
        idform = self.env.ref('base.view_attachment_form')
        idtree = self.env.ref('base.view_attachment_tree')
        kanban = self.env.ref('mail.view_document_file_kanban')
        return {
            'view_type': 'form',
            'view_mode': 'kanban, tree, form',
            'res_model': 'ir.attachment',
            'views': [(kanban.id, 'kanban'), (idtree.id, 'tree'),
                      (idform.id, 'form')],
            'search_view_id': search_view.id,
            'view_id': kanban.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': "[('id','in',[" +
            ','.join(map(str, attachmen_lst)) + "])]",
            'context': self.env.context,
            }
