from odoo import models, fields

class Carrier(models.Model):
    _name = 'purchase.order.carrier'
    _description = 'Carrier for Purchase Orders'

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Carrier name must be unique!')
    ]

    name = fields.Char(
        string="Carrier Name", 
        required=True,
    )
