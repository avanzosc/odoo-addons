from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    employee_id = fields.Many2one(
        'hr.employee', 
        string='Responsible Employee'
    )
