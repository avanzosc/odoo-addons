# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartnerBankMandateGenerator(models.TransientModel):
    _name = "res.partner.bank.mandate.generator"
    _description = "Wizard to generate mandates"

    def _default_mandate_format(self):
        default_dict = self.env["account.banking.mandate"].default_get(["format"])
        return default_dict.get("format")

    def _default_mandate_type(self):
        default_dict = self.env["account.banking.mandate"].default_get(["type"])
        return default_dict.get("type")

    def _default_mandate_scheme(self):
        default_dict = self.env["account.banking.mandate"].default_get(["scheme"])
        return default_dict.get("scheme")

    def _default_mandate_recurrent_sequence_type(self):
        default_dict = self.env["account.banking.mandate"].default_get(
            ["recurrent_sequence_type"]
        )
        return default_dict.get("recurrent_sequence_type")

    bank_ids = fields.Many2many(
        comodel_name="res.partner.bank", string="Banks", required=True
    )
    mandate_format = fields.Selection(
        selection="_get_format_selection",
        string="Mandate Format",
        default=_default_mandate_format,
        required=True,
    )
    mandate_type = fields.Selection(
        selection="_get_type_selection",
        string="Type of Mandate",
        default=_default_mandate_type,
    )
    mandate_scheme = fields.Selection(
        selection="_get_scheme_selection",
        string="Scheme",
        default=_default_mandate_scheme,
    )
    mandate_recurrent_sequence_type = fields.Selection(
        selection="_get_recurrent_sequence_type_selection",
        string="Sequence Type for Next Debit",
        default=_default_mandate_recurrent_sequence_type,
    )
    signed = fields.Boolean()
    validate = fields.Boolean()

    @api.model
    def default_get(self, fields_list):
        res = super(ResPartnerBankMandateGenerator, self).default_get(fields_list)
        if self.env.context.get("active_model") == "res.partner.bank":
            res.update({"bank_ids": [(6, 0, self.env.context.get("active_ids"))]})
        return res

    @api.model
    def _get_format_selection(self):
        return self.env["account.banking.mandate"].fields_get(allfields=["format"])[
            "format"
        ]["selection"]

    @api.model
    def _get_type_selection(self):
        return self.env["account.banking.mandate"].fields_get(allfields=["type"])[
            "type"
        ]["selection"]

    @api.model
    def _get_scheme_selection(self):
        return self.env["account.banking.mandate"].fields_get(allfields=["scheme"])[
            "scheme"
        ]["selection"]

    @api.model
    def _get_recurrent_sequence_type_selection(self):
        return self.env["account.banking.mandate"].fields_get(
            allfields=["recurrent_sequence_type"]
        )["recurrent_sequence_type"]["selection"]

    @api.onchange("signed")
    def _onchange_signed(self):
        for wizard in self:
            if not wizard.signed and wizard.validate:
                wizard.validate = False

    @api.onchange("validate")
    def _onchange_validate(self):
        for wizard in self:
            if wizard.validate and not wizard.signed:
                wizard.signed = True

    def button_generate_mandates(self):
        mandate_obj = self.env["account.banking.mandate"]
        signature_date = (
            fields.Date.context_today(self) if (self.signed or
                                                self.validate) else False)
        for bank in self.bank_ids:
            if not bank._check_active_mandate():
                mandate_dict = bank._get_mandate_vals()
                mandate_dict.update(
                    {
                        "format": self.mandate_format,
                        "type": self.mandate_type,
                        "scheme": self.mandate_scheme,
                        "recurrent_sequence_type": self.mandate_recurrent_sequence_type,
                    }
                )
                if signature_date:
                    mandate_dict.update(
                        {
                            "signature_date": signature_date,
                        }
                    )
                mandate = mandate_obj.create(mandate_dict)
                if self.validate:
                    mandate.validate()
