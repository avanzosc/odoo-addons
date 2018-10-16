# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountAnalyticline(models.Model):
    _inherit = 'account.analytic.line'

    invoice_id = fields.Many2one(
        string='Invoice', comodel_name='account.invoice',
        related='move_id.invoice_id', store=True)
    invoice_number = fields.Char(
        string='Invoice Number',
        related='move_id.invoice_id.number', store=True)
    invoice_reference = fields.Char(
        string='Invoice Vendor Reference',
        related='move_id.invoice_id.reference', store=True)
    invoice_partner_id = fields.Many2one(
        string='Invoice Partner', comodel_name='res.partner',
        related='move_id.invoice_id.partner_id', store=True)
