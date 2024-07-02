from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    employee_id = fields.Many2one("hr.employee", string="Responsible Employee")
