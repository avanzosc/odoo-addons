# Copyright (c) 2017 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class WizardImportPartnerDocument(models.TransientModel):
    _name = 'wizard.import.partner.document'

    def import_partner_document(self):
        partner_obj = self.env['res.partner']
        doc_tmpl_obj = self.env['partner.document.template']
        doc_obj = self.env['partner.document']
        document_tmpls = doc_tmpl_obj.search([]).filtered(
            lambda x: x.company_id.id == self.env.user.company_id.id or not
            x.company_id)
        for partner_id in self.env.context['active_ids']:
            partner = partner_obj.browse(partner_id)
            document_tmpls = document_tmpls.filtered(
                lambda r: partner.customer and
                r.customer_document == partner.customer or partner.supplier and
                r.supplier_document == partner.supplier or
                partner.employee and r.employee_document == partner.employee)
            partner_lines = partner.document_lines.mapped(
                'document_tmpl_id').ids or []
            document_tmplp_ids = document_tmpls.filtered(
                lambda r: r.id not in partner_lines).ids
            for tmpl_id in document_tmplp_ids:
                doc_obj.create({'document_tmpl_id': tmpl_id,
                                'partner_id': partner_id,
                                })
        return {}
