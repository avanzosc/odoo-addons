# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountPaymentLineCreate(models.TransientModel):
    _inherit = 'account.payment.line.create'

    bank_partner_id = fields.Many2one(
        comodel_name="res.partner", string="Bank Account Holder")

    @api.model
    def default_get(self, field_list):
        res = super(AccountPaymentLineCreate, self).default_get(field_list)
        context = self.env.context
        order = self.env['account.payment.order'].browse(context['active_id'])
        res.update({
            "bank_partner_id": order.company_partner_bank_id.partner_id.id,
        })
        return res

    @api.multi
    def _prepare_move_line_domain(self):
        self.ensure_one()
        domain = super(AccountPaymentLineCreate,
                       self)._prepare_move_line_domain()
        if self.bank_partner_id:
            domain += [("school_id", '=', self.bank_partner_id.id)]
        return domain
