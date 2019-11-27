# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartnerBankMandateGenerator(models.TransientModel):
    _name = 'res.partner.bank.mandate.generator'

    @api.model
    def _get_format_selection(self):
        return self.env['account.banking.mandate'].fields_get(
            allfields=['format'])['format']['selection']

    @api.model
    def _get_type_selection(self):
        return self.env['account.banking.mandate'].fields_get(
            allfields=['type'])['type']['selection']

    bank_ids = fields.Many2many(
        comodel_name='res.partner.bank', string='Banks')
    format = fields.Selection(
        selection=_get_format_selection, string='Mandate Format')
    type = fields.Selection(
        selection=_get_type_selection, string='Type of Mandate')
    scheme = fields.Selection()
    recurrent_sequence_type = fields.Selection()
    signed = fields.Boolean()
    validate = fields.Boolean()
