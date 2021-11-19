# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contact_type_id = fields.Many2one(
        string='Contact type', comodel_name='res.partner.type',
        related='partner_invoice_id.contact_type_id', store=True)
    analytic_account_id = fields.Many2one(
        string='Analytic Account', comodel_name='account.analytic.account',
        related='contact_type_id.analytic_account_id', store=True,
        check_company=True)
