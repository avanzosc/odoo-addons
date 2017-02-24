# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields


class HrPaymentType(models.Model):
    _name = "hr.payment.type"

    name = fields.Char(string='Name', translate=True)


class HrPaymentPeriodicity(models.Model):
    _name = 'hr.payment.periodicity'

    name = fields.Char(string='Name', translate=True)


class HrContractCompensation(models.Model):
    _name = 'hr.contract.compensation'

    @api.multi
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    payment_type_id = fields.Many2one(
        comodel_name='hr.payment.type', string='Payment type')
    periodicity_id = fields.Many2one(
        comodel_name='hr.payment.periodicity', string='Periodicity')
    amount = fields.Float(string='Amount')
    currency_id = fields.Many2one(
        comodel_name='res.currency', string='Currency',
        default=_default_currency_id)
    contract_id = fields.Many2one(
        comodel_name='hr.contract', string='Contract')
