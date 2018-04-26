from odoo import fields, models


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    analytic_line_kind_id = fields.Many2one(
        comodel_name='account.analytic.line.kind',
        string="Account analytic line kind")


class AccountAnalyticLineKind(models.Model):

    _name = "account.analytic.line.kind"

    name = fields.Char(string="Account analytic line kind", required=True)
