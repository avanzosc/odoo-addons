# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from odoo.api import Environment
from odoo import SUPERUSER_ID


def assign_old_sequences(cr, registry):
    with Environment.manage():
        env = Environment(cr, SUPERUSER_ID, {})

        sequence_model = env['ir.sequence']

        accounts = env['account.analytic.account'].with_context(
            active_test=False).search([('code', '=', '')], order="id")
        for account in accounts:
            account.code = sequence_model.next_by_code('account.analytic.code')
