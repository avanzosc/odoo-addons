# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountAnalyticTemplate(models.Model):
    _name = "account.analytic.template"
    _description="Account Anlytic Template"

    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account")
    account_analytic_id = fields.Many2one(
        string="Account Anlytic",
        comodel_name="account.analytic.account")
    percentage = fields.Float(
        string="%")
