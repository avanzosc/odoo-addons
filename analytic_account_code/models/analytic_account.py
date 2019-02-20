# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from odoo import api, fields, models


class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    code = fields.Char(
        default="/", readonly=True, copy=False)

    @api.model
    def create(self, values):
        if values.get('code', '/') == '/':
            values['code'] = self.env['ir.sequence'].next_by_code(
                'account.analytic.code')
        return super(AnalyticAccount, self).create(values)
