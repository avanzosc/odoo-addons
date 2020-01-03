# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartnerBankMandateGenerator(models.TransientModel):
    _name = "res.partner.bank.mandate.generator"
    _description = "Wizard to generate mandates"

    def _default_mandate_format(self):
        default_dict = self.env["account.banking.mandate"].default_get([
            "format"])
        return default_dict.get("format")

    def _default_mandate_type(self):
        default_dict = self.env["account.banking.mandate"].default_get([
            "type"])
        return default_dict.get("type")

    def _default_mandate_scheme(self):
        default_dict = self.env["account.banking.mandate"].default_get([
            "scheme"])
        return default_dict.get("scheme")

    def _default_mandate_recurrent_sequence_type(self):
        default_dict = self.env["account.banking.mandate"].default_get([
            "recurrent_sequence_type"])
        return default_dict.get("recurrent_sequence_type")

    bank_ids = fields.Many2many(
        comodel_name="res.partner.bank", string="Banks", required=True)
    mandate_format = fields.Selection(
        selection="_get_format_selection", string="Mandate Format",
        default=_default_mandate_format, required=True)
    mandate_type = fields.Selection(
        selection="_get_type_selection", string="Type of Mandate",
        default=_default_mandate_type)
    mandate_scheme = fields.Selection(
        selection="_get_scheme_selection", string="Scheme",
        default=_default_mandate_scheme)
    mandate_recurrent_sequence_type = fields.Selection(
        selection="_get_recurrent_sequence_type_selection",
        string="Sequence Type for Next Debit",
        default=_default_mandate_recurrent_sequence_type)
    signed = fields.Boolean()
    validate = fields.Boolean()

    @api.model
    def default_get(self, fields_list):
        res = super(ResPartnerBankMandateGenerator, self).default_get(
            fields_list)
        if self.env.context.get('active_model') == 'res.partner.bank':
            res.update({'bank_ids': self.env.context.get('active_ids')})
        return res

    @api.model
    def _get_format_selection(self):
        return self.env["account.banking.mandate"].fields_get(
            allfields=["format"])["format"]["selection"]

    @api.model
    def _get_type_selection(self):
        return self.env["account.banking.mandate"].fields_get(
            allfields=["type"])["type"]["selection"]

    @api.model
    def _get_scheme_selection(self):
        return self.env["account.banking.mandate"].fields_get(
            allfields=["scheme"])["scheme"]["selection"]

    @api.model
    def _get_recurrent_sequence_type_selection(self):
        return self.env["account.banking.mandate"].fields_get(
            allfields=["recurrent_sequence_type"]
        )["recurrent_sequence_type"]["selection"]
