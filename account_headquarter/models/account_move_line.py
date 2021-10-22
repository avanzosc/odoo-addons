# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    headquarter_id = fields.Many2one(
        string='Headquarter', comodel_name='res.partner',
        domain="[('headquarter','=', True)]")

    def write(self, values):
        result = super(AccountMoveLine, self).write(values)
        if 'headquarter_id' in values:
            for line in self:
                line.update_analytic_lines_hearquarter()
        return result

    def update_analytic_lines_hearquarter(self):
        for line in self:
            if line.analytic_line_ids:
                vals = {'headquarter_id': (line.headquarter_id.id
                                           if line.headquarter_id else False)}
                line.analytic_line_ids.write(vals)
