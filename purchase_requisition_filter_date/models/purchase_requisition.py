from odoo import fields, models


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    date_from = fields.Date(string="From")
    date_to = fields.Date(string="To")
