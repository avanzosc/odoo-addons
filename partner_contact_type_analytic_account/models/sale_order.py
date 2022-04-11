# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contact_type_id = fields.Many2one(
        string='Contact type', comodel_name='res.partner.type',
        related='partner_invoice_id.contact_type_id', store=True)
    analytic_account_id = fields.Many2one(
        string='Analytic Account', comodel_name='account.analytic.account',
        compute='_compute_analytic_account_id', store=True, related=False,
        company_dependent=False, check_company=False, domain=False)

    @api.depends('partner_invoice_id', 'partner_invoice_id.contact_type_id',
                 'contact_type_id.analytic_account_id')
    def _compute_analytic_account_id(self):
        for sale in self:
            if (sale.partner_invoice_id.contact_type_id and
                    sale.partner_invoice_id.contact_type_id.with_company(
                        sale.company_id.id).analytic_account_id):
                sale.analytic_account_id = (
                    sale.partner_invoice_id.contact_type_id.with_company(
                        sale.company_id.id).analytic_account_id.id)
