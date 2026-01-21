# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api

class AgreementPenaltyType(models.Model):
    _name = 'agreement.penalty.type'
    _description = 'Agreement Penalty Type'

    name = fields.Char(related="penalty_type_id.name", readonly=True)
    agreement_id = fields.Many2one('agreement', required=True, ondelete='cascade')
    penalty_type_id = fields.Many2one('penalty.type', required=True)
        
    product_id = fields.Many2one(
        'product.product', 
        related='penalty_type_id.product_id', 
        string='Product', 
        readonly=True,
        store=True
    )

    penalty_price = fields.Float(
        string='Penalty Price', 
        digits='Product Price',
        help="Base price for this penalty. Auto-filled from product list price."
    )

    percentage = fields.Float(
        string='Percentage', 
        digits=(5, 2), 
        help="Penalty percentage (e.g. 10%)"
    )

    quantity = fields.Float(default=1.0)
    term = fields.Selection([
        ('days', 'Days'),
        ('months', 'Months'),
        ('years', 'Years')
    ], string='Term')
    notes = fields.Text()

    @api.onchange('penalty_type_id')
    def _onchange_penalty_type_id(self):
        if self.penalty_type_id and self.penalty_type_id.product_id:
            self.penalty_price = self.penalty_type_id.product_id.list_price
