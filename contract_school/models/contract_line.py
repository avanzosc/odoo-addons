# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ContractLine(models.Model):
    _inherit = 'contract.line'

    payment_percentage = fields.Float(string='Percentage', default=100.0)
    user_id = fields.Many2one(
        comodel_name='res.users', string='User')
    observations = fields.Text(string='Observations')

    @api.multi
    @api.depends('quantity', 'price_unit', 'discount', 'payment_percentage')
    def _compute_price_subtotal(self):
        super(ContractLine, self)._compute_price_subtotal()
        for line in self.filtered(lambda x: x.payment_percentage != 100.0):
            line.price_subtotal = (
                line.price_subtotal * line.payment_percentage) / 100

    @api.model
    def _prepare_invoice_line(self, invoice_id=False):
        self.ensure_one()
        res = super(ContractLine, self)._prepare_invoice_line(
            invoice_id=invoice_id)
        res['payment_percentage'] = self.payment_percentage
        return res
