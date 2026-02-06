# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api

class Agreement(models.Model):
    _inherit = 'agreement'
    
    def _apply_early_termination_penalties(self):
        for agreement in self:
            journal = (
                agreement.sale_type_id.journal_id
                if agreement.sale_type_id and agreement.sale_type_id.journal_id
                else self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
            )
        
            partner = agreement.partner_id
        
            closed_subscriptions = self.env['sale.subscription'].search([
                ('agreement_id', '=', agreement.id),
                ('date', '!=', False),
                ('stage_id.category', '=', 'closed'),
            ])
        
            for penalty_line in agreement.agreement_penalty_ids:
                penalty_quantity = 0
                penalty_amount = 0.0

                if penalty_line.penalty_type_id.name == 'Early Termination':
                    for sub in closed_subscriptions:
                        result = sub._early_termination_penalties(
                            penalty_type_id=penalty_line.penalty_type_id.id,
                            penalty_percent=penalty_line.penalty_percentage,
                            penalty_permanence=penalty_line.number
                        )
                        penalty_quantity += result['quantity']
                        penalty_amount += result['amount']

                if penalty_quantity > 0 and penalty_amount > 0:
                    self.env['account.penalty'].create({
                        'agreement_id': agreement.id,
                        'name': f'{penalty_line.penalty_type_id.name}',
                        'quantity': penalty_quantity,
                        'amount': penalty_amount,
                        'invoice_date': fields.Date.today(),
                        'penalty_type_id': penalty_line.penalty_type_id.id,
                        'product_id': penalty_line.penalty_type_id.product_id.id if penalty_line.penalty_type_id.product_id else False,
                        'partner_id': partner.id if partner else False,
                        'journal_id': journal.id if journal else False,
                    })
