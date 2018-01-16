# Copyright (c) 2017 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PartnerDocumentTemplate(models.Model):
    _name = 'partner.document.template'
    _description = "Partner Document"

    name = fields.Char(string='Document Name', required=True)
    customer_document = fields.Boolean(string='Customer Document')
    supplier_document = fields.Boolean(string='Supplier Document')
    employee_document = fields.Boolean(string='Employee Document')
    payment_req = fields.Boolean(string='Payment Required')
    site_entry_req = fields.Boolean(string='Construction Site Entry Required')
    agreement_req = fields.Boolean(string="Agreement Required")
    company_id = fields.Many2one(
        'res.company', string='Company', copy=False,
        default=lambda self: self.env['res.company']._company_default_get())


class PartnerDocument(models.Model):
    _name = 'partner.document'
    _description = "Partner Document"

    @api.onchange('document_attachment')
    def _onchange_document_attachment(self):
        partner_id = self.env.context.get('set_partner_id', False)
        if self.document_attachment and partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            self.document_attachment.write({
                'res_id': partner.id,
                'res_model': 'res.partner',
                'res_name': partner.name
                })

    def write(self, vals):
        res = super(PartnerDocument, self).write(vals)
        if 'document_attachment' in vals and vals['document_attachment']:
            self.document_attachment.write({
                'res_id': self.partner_id.id,
                'res_model': 'res.partner',
                'res_name': self.partner_id.name
                })
        return res

    document_tmpl_id = fields.Many2one(
        comodel_name='partner.document.template',
        string='Documentation template')
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner')
    document_attachment = fields.Many2one(
        comodel_name='ir.attachment',
        string='Partner Document attachment')
    document_date = fields.Datetime(
        string="Document Date",
        )
    received_date = fields.Datetime(
        string="Received Date",
        )
    validate_date = fields.Datetime(
        string="Validate Date",
        )
    notes = fields.Text(string='Notes')
    customer_document = fields.Boolean(
        string='Customer Document', comodel_name='partner.document.template',
        related='document_tmpl_id.customer_document', store=True,
        readonly=True)
    supplier_document = fields.Boolean(
        string='Supplier Document', comodel_name='partner.document.template',
        related='document_tmpl_id.supplier_document', store=True,
        readonly=True)
    employee_document = fields.Boolean(
        string='Employee Document', comodel_name='partner.document.template',
        related='document_tmpl_id.employee_document', store=True,
        readonly=True)
    payment_req = fields.Boolean(
        string='Payment Required', comodel_name='partner.document.template',
        related='document_tmpl_id.payment_req', store=True, readonly=True)
    site_entry_req = fields.Boolean(
        string='Construction Site Entry Required',
        comodel_name='partner.document.template',
        related='document_tmpl_id.site_entry_req', store=True, readonly=True)
    agreement_req = fields.Boolean(
        string="Agreement Required", comodel_name='partner.document.template',
        related='document_tmpl_id.agreement_req', store=True, readonly=True)

    @api.multi
    def show_attachment(self):
        search_view = self.env.ref('base.view_attachment_search')
        kanban = self.env.ref('mail.view_document_file_kanban')
        return {
            'view_type': 'form',
            'view_mode': 'kanban',
            'res_model': 'ir.attachment',
            'views': [(kanban.id, 'kanban')],
            'search_view_id': search_view.id,
            'view_id': kanban.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': "[('id','in',[{}])]".format(self.document_attachment.id),
            'context': self.env.context,
            }
